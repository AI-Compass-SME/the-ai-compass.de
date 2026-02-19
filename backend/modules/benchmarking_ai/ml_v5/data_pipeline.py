
import os
import pandas as pd
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()

class DataPipeline:
    def __init__(self):
        self.conn = None
        self._connect()

    def _connect(self):
        import time
        retries = 3
        for i in range(retries):
            try:
                # Try DATABASE_URL first (full connection string)
                db_url = os.getenv("DATABASE_URL")
                if db_url:
                    self.conn = psycopg2.connect(db_url)
                else:
                    # Fallback to individual parameters
                    self.conn = psycopg2.connect(
                        user=os.getenv("user"),
                        password=os.getenv("password"),
                        host=os.getenv("host"),
                        port=os.getenv("port"),
                        dbname=os.getenv("dbname")
                    )
                print("Connected to Database")
                return
            except Exception as e:
                print(f"Connection Attempt {i+1} failed: {e}")
                if i < retries - 1:
                    time.sleep(2)
        print("Final Connection Error: Could not connect to DB.")

    def fetch_data(self):
        """Fetches and merges data into a single DataFrame."""
        if not self.conn:
            return None

        queries = {
            "responses": "SELECT * FROM responses",
            "companies": "SELECT * FROM companies",
            "response_items": "SELECT * FROM response_items",
            "questions": "SELECT * FROM questions",
            "dimensions": "SELECT * FROM dimensions",
            "cluster_profiles": "SELECT * FROM cluster_profiles ORDER BY cluster_id",
        }
        
        dfs = {}
        cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        
        for name, query in queries.items():
            cur.execute(query)
            dfs[name] = pd.DataFrame(cur.fetchall())
        
        cur.close()
        return dfs
    
    def get_question_metadata(self, dfs):
        """
        Extracts question metadata from the fetched dataframes.
        Returns a DataFrame with question specifics needed for granular recommendations.
        """
        questions = dfs['questions']
        dimensions = dfs['dimensions']
        
        # Merge to get dimension names
        q_meta = questions.merge(dimensions, on='dimension_id', how='left')
        
        # Select relevant columns for downstream logic
        # Renaming 'weight' to 'question_weight', 'header' to 'tactical_theme'
        q_meta = q_meta.rename(columns={
            'weight': 'question_weight', 
            'header': 'tactical_theme',
            'type': 'question_type'
        })
        
        return q_meta[['question_id', 'question_text', 'tactical_theme', 'question_type', 'question_weight', 'dimension_name']]

    def create_matrices(self, dfs):
        """
        Creates QuestionMatrix and DimensionMatrix.
        Returns:
            question_matrix (pd.DataFrame): Index=company_id, Cols=question_text/id
            dimension_matrix (pd.DataFrame): Index=company_id, Cols=dimension_name
            cluster_profiles (pd.DataFrame): Cluster naming metadata
            question_metadata (pd.DataFrame): Rich metadata for questions
        """
        # Unpack
        responses = dfs['responses']
        items = dfs['response_items']
        questions = dfs['questions']
        dimensions = dfs['dimensions']
        companies = dfs['companies']

        # Let's fetch answers table too to map weights
        cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute("SELECT * FROM answers")
        answers_ref = pd.DataFrame(cur.fetchall())
        cur.close()

        # 1. Flatten Items and merge with metadata
        items_exploded = items.explode('answers')
        items_exploded = items_exploded.rename(columns={'answers': 'answer_id'})
        
        # Merge to get answer weights
        full_df = items_exploded.merge(answers_ref, on=['answer_id', 'question_id'], how='left')
        full_df = full_df.merge(questions, on='question_id', how='left')
        full_df = full_df.merge(dimensions, on='dimension_id', how='left')
        full_df = full_df.merge(responses, on='response_id', how='left')
        
        # 2. Calculate Reference Weights
        ans_stats = answers_ref.groupby('question_id').agg(
            total_possible_weight=('answer_weight', 'sum'),
            max_possible_weight=('answer_weight', 'max')
        ).reset_index()
        
        full_df = full_df.merge(ans_stats, on='question_id', how='left')

        # 3. Aggregating Selected Answer Weights per Question per Company
        grouped_questions = full_df.groupby([
            'company_id', 'question_id', 'dimension_name', 'weight', 'type', 
            'total_possible_weight', 'max_possible_weight'
        ])['answer_weight'].sum().reset_index()
        
        grouped_questions = grouped_questions.rename(columns={'weight': 'question_weight', 'answer_weight': 'sum_selected_weight'})

        # 4. Apply Scoring Logic
        def calculate_question_score(row):
            if row['type'] == 'Checklist':
                total_w = row['total_possible_weight']
                ratio = row['sum_selected_weight'] / total_w if total_w > 0 else 0
            else:
                max_w = row['max_possible_weight']
                ratio = row['sum_selected_weight'] / max_w if max_w > 0 else 0
            
            return (ratio * row['question_weight']) / 100

        grouped_questions['question_score_contrib'] = grouped_questions.apply(calculate_question_score, axis=1)
        
        # Keep a 1-5 version for the Question Matrix for readability and 'weighted impact' calc
        grouped_questions['score_1to5'] = (grouped_questions['question_score_contrib'] / (grouped_questions['question_weight'] / 100)) * 4 + 1
        grouped_questions['score_1to5'] = grouped_questions['score_1to5'].fillna(1.0)

        # 5. Question Matrix (1-5 Scale)
        q_matrix = grouped_questions.pivot_table(
            index='company_id', 
            columns='question_id', 
            values='score_1to5', 
            aggfunc='mean'
        ).fillna(1.0)

        # 6. Dimension Matrix (Weighted Average -> 1-5 Scale)
        dim_groups = grouped_questions.groupby(['company_id', 'dimension_name'])
        
        dim_results = dim_groups.apply(
            lambda x: (x['question_score_contrib'].sum() / (x['question_weight'].sum() / 100)) * 4 + 1 if x['question_weight'].sum() > 0 else 1.0
        ).reset_index(name='dimension_score')
        
        d_matrix = dim_results.pivot_table(
            index='company_id', 
            columns='dimension_name', 
            values='dimension_score'
        ).fillna(1.0)
        
        if 'General Psychology' in d_matrix.columns:
            d_matrix = d_matrix.drop(columns=['General Psychology'])
        
        # 7. Metadata 
        q_meta = self.get_question_metadata(dfs)
        
        return q_matrix, d_matrix, dfs.get('cluster_profiles', pd.DataFrame()), q_meta

if __name__ == "__main__":
    dp = DataPipeline()
    dfs = dp.fetch_data()
    if dfs:
        qm, dm, profiles, q_meta = dp.create_matrices(dfs)
        print("Question Matrix Shape:", qm.shape)
        print("Dimension Matrix Shape:", dm.shape)
        print("Profiles Loaded:", len(profiles))
        print("Question Metadata:", q_meta.head())
