import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Setup Environment & Imports
# Add project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(root_path)

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

try:
    from benchmarking_ai.ml_v5.inference import InferenceEngine
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

# 2. Connect to DB
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("DATABASE_URL not set")
    sys.exit(1)

engine = create_engine(db_url.replace("postgres://", "postgresql://"))
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 3. Fetch Data for Response 4
response_id = 4
print(f"--- Debugging Response {response_id} ---")

# We need to replicate the exact queries from results.py
query_items = f"SELECT * FROM response_items WHERE response_id = {response_id}"
query_questions = "SELECT * FROM questions"
query_dims = "SELECT * FROM dimensions"
query_answers = "SELECT * FROM answers"

try:
    df_items = pd.read_sql(query_items, engine)
    df_questions = pd.read_sql(query_questions, engine)
    df_dims = pd.read_sql(query_dims, engine)
    df_answers_ref = pd.read_sql(query_answers, engine)
    
    # Check if we have data
    if df_items.empty:
        print("No items found for this response.")
        sys.exit(0)

    # 4. Replicate Logic
    # Flatten
    # Note: df_items['answers'] might be list or string depending on driver. 
    # Psycopg2 usually returns lists for ARRAY types.
    
    df_items_exploded = df_items.explode('answers')
    df_items_exploded = df_items_exploded.rename(columns={'answers': 'answer_id'})
    df_items_exploded['answer_id'] = df_items_exploded['answer_id'].fillna(0).astype(int)

    # Merge
    full_df = df_items_exploded.merge(df_answers_ref, on=['answer_id', 'question_id'], how='left')
    full_df = full_df.merge(df_questions, on='question_id', how='left')
    full_df = full_df.merge(df_dims, on='dimension_id', how='left')

    # Aggregating
    ans_stats = df_answers_ref.groupby('question_id').agg(
        total_possible_weight=('answer_weight', 'sum'),
        max_possible_weight=('answer_weight', 'max')
    ).reset_index()
    full_df = full_df.merge(ans_stats, on='question_id', how='left')

    # Summing Weights
    grouped_q = full_df.groupby([
        'question_id', 'dimension_name', 'weight', 'type', 
        'total_possible_weight', 'max_possible_weight', 'question_text', 'header'
    ])['answer_weight'].sum().reset_index().rename(columns={'answer_weight': 'sum_selected_weight'})
    
    # Rename cols to match code
    grouped_q = grouped_q.rename(columns={'weight': 'question_weight', 'type': 'question_type', 'header': 'tactical_theme'})

    def calculate_question_score(row):
        if row['question_type'] == 'Checklist':
            total_w = row['total_possible_weight']
            ratio = row['sum_selected_weight'] / total_w if total_w > 0 else 0
        else:
            max_w = row['max_possible_weight']
            ratio = row['sum_selected_weight'] / max_w if max_w > 0 else 0
        return (ratio * row['question_weight']) / 100

    grouped_q['question_score_contrib'] = grouped_q.apply(calculate_question_score, axis=1)

    dim_groups = grouped_q.groupby('dimension_name')
    dim_results = dim_groups.apply(
        lambda x: (x['question_score_contrib'].sum() / (x['question_weight'].sum() / 100)) * 4 + 1 
        if x['question_weight'].sum() > 0 else 1.0
    )
    
    if 'General Psychology' in dim_results.index:
        dim_results = dim_results.drop('General Psychology')

    grouped_q['score_1to5'] = (grouped_q['question_score_contrib'] / (grouped_q['question_weight'] / 100)) * 4 + 1
    grouped_q['score_1to5'] = grouped_q['score_1to5'].fillna(1.0)
    
    # SANITIZE
    grouped_q['tactical_theme'] = grouped_q['tactical_theme'].fillna("")
    grouped_q['question_text'] = grouped_q['question_text'].fillna("")
    grouped_q['question_type'] = grouped_q['question_type'].fillna("")

    print("--- Inputs Prepared ---")
    print(dim_results)
    
    # 5. Run Inference
    print("\n--- Running Inference ---")
    engine = InferenceEngine()
    
    res = engine.run_analysis(dim_results, grouped_q)
    print("\n--- SUCCESS ---")
    print(res.keys())

except Exception as e:
    print("\n--- CRASH DETECTED ---")
    import traceback
    traceback.print_exc()
