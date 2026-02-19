"""
Script to retrain models and regenerate v5.1 report with theme-specific explanations
"""

import subprocess
import sys

print("=" * 60)
print("Retraining ML v5 models with theme-specific explanations...")
print("=" * 60)

# Step 1: Train models
print("\n[1/2] Training models...")
result = subprocess.run(
    [sys.executable, "-m", "benchmarking_ai.ml_v5.train_models"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
    sys.exit(1)

# Step 2: Generate verification report
print("\n[2/2] Generating verification report...")
result = subprocess.run(
    [sys.executable, "-m", "benchmarking_ai.ml_v5.verify_representatives"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ Complete! Check cluster_representative_test_findings_v5.1.md")
print("=" * 60)
