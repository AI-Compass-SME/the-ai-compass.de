import sys
import os

# Current: backend/
# Root is ../../
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(root_path)

print(f"Added to path: {root_path}")
print(f"Exists? {os.path.exists(root_path)}")
print(f"Contents of root: {os.listdir(root_path)}")

try:
    import benchmarking_ai
    print("SUCCESS: Imported benchmarking_ai")
except ImportError as e:
    print(f"FAILURE: benchmarking_ai - {e}")

try:
    from benchmarking_ai.ml_v5.inference import InferenceEngine
    print("SUCCESS: Imported InferenceEngine")
    
    eng = InferenceEngine()
    print("SUCCESS: Instantiated Engine")
except Exception as e:
    print(f"FAILURE: InferenceEngine - {e}")
    import traceback
    traceback.print_exc()
