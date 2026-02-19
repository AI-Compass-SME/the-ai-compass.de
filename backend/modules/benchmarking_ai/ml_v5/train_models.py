
import os
import pandas as pd
from benchmarking_ai.ml_v5.data_pipeline import DataPipeline
from benchmarking_ai.ml_v5.models import ClusterEngine, StrategicGapAnalyzer, RoadmapGenerator

def train_and_save():
    print("Starting Training Pipeline [ML v5]...")
    
    # 1. Fetch Data
    dp = DataPipeline()
    dfs = dp.fetch_data()
    q_matrix, d_matrix, profiles, q_meta = dp.create_matrices(dfs)
    
    print(f"Data Loaded. Companies: {len(d_matrix)}")
    
    # Prepare industry data for percentile calculation
    # Get industry info from companies dataframe
    companies_df = dfs['companies']
    industry_data = pd.DataFrame({
        'company_id': d_matrix.index,
        'industry': companies_df.set_index('company_id').loc[d_matrix.index, 'industry'],
        'total_maturity': d_matrix.mean(axis=1)
    }).reset_index(drop=True)
    
    # Ensure artifacts dir exists in the module folder
    # Relative to project root (since we run with python -m from root)
    output_dir = "benchmarking_ai/ml_v5/model_artifacts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 2. Train Cluster Engine with industry data
    ce = ClusterEngine()
    ce.fit(d_matrix, profiles, industry_data=industry_data)
    ce.save_model(f"{output_dir}/v5")
    print("Cluster Engine trained and saved.")
    
    # 3. Train Strategic Gap Analyzer
    sga = StrategicGapAnalyzer()
    sga.fit(d_matrix)
    sga.save_model(f"{output_dir}/v5")
    print("Strategic Gap Analyzer trained and saved.")
    
    # 4. Train Roadmap Generator
    # Add industry column for industry-specific benchmarking
    d_matrix_with_industry = d_matrix.copy()
    d_matrix_with_industry['industry'] = companies_df.set_index('company_id').loc[d_matrix.index, 'industry']
    
    rg = RoadmapGenerator()
    rg.fit(d_matrix_with_industry, q_matrix)
    rg.save_model(f"{output_dir}/v5")
    print("Roadmap Generator trained and saved.")
    
    print("All ML v5 models successfully trained.")

if __name__ == "__main__":
    train_and_save()
