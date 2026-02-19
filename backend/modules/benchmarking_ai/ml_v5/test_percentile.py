"""
Test script to retrain models with industry percentile and verify output
"""

import subprocess
import sys

print("=" * 60)
print("Retraining ML v5 models with industry percentile support...")
print("=" * 60)

# Step 1: Train models
print("\n[1/2] Training models with industry data...")
result = subprocess.run(
    [sys.executable, "-m", "benchmarking_ai.ml_v5.train_models"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
    sys.exit(1)

# Step 2: Test API with percentile
print("\n[2/2] Testing API with percentile calculation...")
result = subprocess.run(
    [sys.executable, "models/test_api.py"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ Complete! Check models/sample_output.json for percentile")
print("=" * 60)
