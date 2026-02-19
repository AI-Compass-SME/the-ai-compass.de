# Industry Percentile Feature - ML v5

## Summary

Added industry-specific percentile ranking to ml_v5 models. This calculates where a company ranks within their industry based on total maturity score.

## Changes Made

### 1. ClusterEngine (`models.py`)
- Added `industry_data` attribute to store company industry information
- Added `calculate_industry_percentile()` method
- Updated `fit()` to accept `industry_data` parameter
- Updated `save_model()` and `load_model()` to persist industry data

### 2. Training Pipeline (`train_models.py`)
- Prepares industry data from companies dataframe
- Passes industry data to `ClusterEngine.fit()`
- Saves industry data with model artifacts

### 3. API (`models/ai_compass_api.py`)
- Calculates industry percentile during analysis
- Includes percentile in cluster_info response
- Returns percentile in JSON format

## Output Format

```json
{
  "cluster_segment": {
    "cluster_id": 0,
    "cluster_name": "4 - The Operational Scaler",
    "coordinates": {"x": 1.20, "y": 0.54},
    "industry_percentile": {
      "percentile_value": "36.70",
      "industry": "Logistics",
      "industry_sample_size": 50
    }
  }
}
```

## Testing

Run the following to retrain models and test:

```bash
python test_percentile.py
```

Or manually:

```bash
# 1. Retrain models with industry data
python -m benchmarking_ai.ml_v5.train_models

# 2. Test API
python test_api.py

# 3. Check output
cat models/sample_output.json | grep -A 5 "industry_percentile"
```

## Next Steps

- Update verification report to display percentile
- Update sample_frontend_response.json with percentile example
