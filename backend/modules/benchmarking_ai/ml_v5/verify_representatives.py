
import pandas as pd
import os
import json
from benchmarking_ai.ml_v5.data_pipeline import DataPipeline
from benchmarking_ai.ml_v5.inference import InferenceEngine

def generate_report():
    print("Verifying ML v5 on Cluster Representatives...")
    
    # 1. Fetch Data
    dp = DataPipeline()
    dfs = dp.fetch_data()
    q_matrix, d_matrix, profiles, q_meta = dp.create_matrices(dfs)
    
    # 2. Initialize Inference Engine
    engine = InferenceEngine(artifacts_path="model_artifacts/v5")
    
    # 3. Representatives
    representatives = [46, 31, 3, 17, 32]
    
    report = "# Verification: 5 Cluster Representatives (ML v5)\n\n"
    report += "This report validates the **ML v5** pipeline, featuring:\n"
    report += "- **Strategic Gap Analysis**: Z-Score Anomalies + Weighted Impact Checks.\n"
    report += "- **Enhanced Roadmap**: 3-Phase Plan with **detailed explanations** for each recommendation.\n"
    report += "- **Narrative Generation**: Automated executive briefings.\n\n"
    
    
    print(f"Total companies in dataset: {len(d_matrix)}")
    print(f"Looking for representatives: {representatives}")
    print(f"Report length before loop: {len(report)} characters")
    
    companies_processed = 0
    
    for cid in representatives:
        # robust check
        if cid not in d_matrix.index:
            # Try string
            if str(cid) in d_matrix.index:
                cid = str(cid)
            elif int(cid) in d_matrix.index:
                cid = int(cid)
            else:
                print(f"Skipping {cid} (Not in data). Available: {d_matrix.index.tolist()[:5]}...")
                continue
            
        print(f"Analyzing Company {cid}...")
        
        # Prepare Inputs
        company_dim = d_matrix.loc[cid]
        
        # Get Company Question Data with metadata
        company_scores = q_matrix.loc[cid].reset_index(name='score_1to5')
        company_q_rich = company_scores.merge(q_meta, on='question_id', how='left')
        
        # Run Analysis
        result = engine.run_analysis(company_dim, company_q_rich)
        
        if "error" in result:
            print(f"Error for {cid}: {result['error']}")
            continue
            
        # Format Output for Markdown Report
        c_name = result['cluster']['cluster_name']
        
        # Calculate industry percentile
        company_industry = dfs['companies'].set_index('company_id').loc[cid, 'industry'] if cid in dfs['companies'].set_index('company_id').index else None
        total_maturity = company_dim.mean()
        percentile_info = None
        if company_industry:
            percentile_info = engine.ce.calculate_industry_percentile(total_maturity, company_industry)
        
        report += f"---\n\n## Cluster Representative: {cid} ({c_name})\n\n"
        
        # Add percentile if available
        if percentile_info:
            report += f"**Industry Percentile**: {percentile_info['percentile_value']}th percentile in {percentile_info['industry']} (n={percentile_info['industry_sample_size']})\n\n"
            report += f"**Better than {percentile_info['percentage']}% of {percentile_info['industry']} companies**\n\n"
        
        # Profile Table
        report += "### 1. Profile Scores\n"
        report += "| Dimension | Score (1-5) |\n| :--- | :---: |\n"
        for dim, score in company_dim.items():
            report += f"| {dim} | {score:.2f} |\n"
        report += "\n"
        
        # Findings
        report += "### 2. Strategic Findings\n"
        for f in result['strategic_findings']:
            icon = "[ANOMALY]" if f['type'] == 'Anomaly' else "[WEAKNESS]"
            report += f"- {icon} **{f['title']}** (Severity: {f['score']:.1f})\n"
            report += f"  - *Context*: {f['context']}\n"
        report += "\n"
        
        # Briefing
        report += "### 3. Executive Briefing\n"
        report += f"> {result['executive_briefing'].replace(chr(10), chr(10)+'> ')}\n\n"
        
        # Roadmap with Explanations
        report += "### 4. Strategic Roadmap (with Explanations)\n"
        roadmap = result['roadmap']
        for phase, items in roadmap.items():
            report += f"#### {phase}\n"
            if not items:
                report += "- *No items (Unexpected)*\n"
            for i in items:
                source_tag = f"[{i['source']}]"
                report += f"- **{i['theme']}** {source_tag} (Impact: {i['impact']:.1f})\n"
                # Add explanation
                if 'explanation' in i:
                    report += f"  - *{i['explanation']}*\n"
        
        report += "\n"
        companies_processed += 1
        print(f"  -> Added to report. Report now {len(report)} characters")
        
    print(f"\nProcessed {companies_processed} companies")
    print(f"Final report length: {len(report)} characters")
    
    # Save Report
    output_path = "benchmarking_ai/ml_v5/cluster_representative_test_findings_v5.1.md"
    print(f"Writing to: {output_path}")
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(report)
        f.flush()
        
    print(f"Verification Report Generated. File size: {len(report)} bytes")

if __name__ == "__main__":
    generate_report()
