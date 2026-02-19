# ML v5 Test & Utility Scripts

This directory contains test and utility scripts for ML v5.

## Scripts

### regenerate_v5_1.py
Retrains ML v5 models and regenerates the v5.1 verification report with theme-specific explanations.

**Usage:**
```bash
cd benchmarking_ai/ml_v5
python regenerate_v5_1.py
```

**What it does:**
1. Trains all ML v5 models (ClusterEngine, StrategicGapAnalyzer, RoadmapGenerator)
2. Generates `cluster_representative_test_findings_v5.1.md` with updated explanations

---

### test_percentile.py
Tests the industry percentile feature by retraining models and running the API.

**Usage:**
```bash
cd benchmarking_ai/ml_v5
python test_percentile.py
```

**What it does:**
1. Trains models with industry data
2. Runs API test to generate `models/sample_output.json` with percentile information

---

## Related Files

- **models/test_api.py** - Tests the production API endpoint
- **verify_representatives.py** - Generates verification reports for cluster representatives
