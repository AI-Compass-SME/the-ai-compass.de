import pandas as pd
from benchmarking_ai.ml_v5.data_pipeline import DataPipeline
from benchmarking_ai.ml_v5.inference import InferenceEngine

print("=== ML v5 Verification Debug ===")

# 1. Fetch Data
dp = DataPipeline()
dfs = dp.fetch_data()
q_matrix, d_matrix, profiles, q_meta = dp.create_matrices(dfs)

# 2. Initialize Inference Engine
engine = InferenceEngine(artifacts_path="model_artifacts/v5")

# 3. Test with Company 46
cid = 46

if cid in d_matrix.index:
    print(f"\n✓ Company {cid} found in dataset")
    
    # Prepare Inputs
    company_dim = d_matrix.loc[cid]
    company_scores = q_matrix.loc[cid].reset_index(name='score_1to5')
    company_q_rich = company_scores.merge(q_meta, on='question_id', how='left')
    
    print(f"  - Dimension scores shape: {company_dim.shape}")
    print(f"  - Question data shape: {company_q_rich.shape}")
    
    # Run Analysis
    result = engine.run_analysis(company_dim, company_q_rich)
    
    if "error" in result:
        print(f"\n✗ Error: {result['error']}")
    else:
        print(f"\n✓ Analysis successful!")
        print(f"  - Cluster: {result['cluster']['cluster_name']}")
        print(f"  - Strategic findings: {len(result['strategic_findings'])}")
        print(f"  - Roadmap phases: {list(result['roadmap'].keys())}")
        
        # Check for explanations
        print(f"\n=== Checking Explanations ===")
        for phase, items in result['roadmap'].items():
            print(f"\n{phase}: {len(items)} items")
            for item in items:
                has_explanation = 'explanation' in item
                print(f"  - {item['theme']}: explanation={'YES' if has_explanation else 'NO'}")
                if has_explanation:
                    print(f"    Preview: {item['explanation'][:100]}...")
else:
    print(f"\n✗ Company {cid} NOT found in dataset")
    print(f"  Available IDs (first 20): {d_matrix.index.tolist()[:20]}")
