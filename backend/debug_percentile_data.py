import pandas as pd
import os
import sys

# Define path to artifact
# Script is in backend/ so we go up to root then down to benchmarking_ai
ARTIFACT_PATH = "../../../benchmarking_ai/ml_v5/model_artifacts/v5_industry_data.pkl"

def inspect_data():
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ARTIFACT_PATH))
    print(f"Loading data from: {abs_path}")
    
    if not os.path.exists(abs_path):
        print("File not found!")
        return

    df = pd.read_pickle(abs_path)
    
    print("\n--- Stats ---")
    if 'industry' in df.columns:
        print(f"Industries: {df['industry'].unique().tolist()}")
        print(f"Industry Counts:\n{df['industry'].value_counts()}")
    else:
        print("Column 'industry' not found!")
    if 'total_maturity' in df.columns:
        print(f"Min: {df['total_maturity'].min()}")
        print(f"Max: {df['total_maturity'].max()}")
        print(f"Mean: {df['total_maturity'].mean()}")
        print(f"Count: {len(df)}")
        print(f"Sample Values: {df['total_maturity'].head().tolist()}")
    else:
        print("Column 'total_maturity' not found!")

if __name__ == "__main__":
    inspect_data()
