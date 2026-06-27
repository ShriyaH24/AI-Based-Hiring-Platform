from pprint import pprint
from parser import load_candidates
from feature_extractor import FeatureExtractor

# 1. Initialize the feature extractor
extractor = FeatureExtractor()

print("Streaming data and extracting features for verification...\n")

# 2. Grab the first available candidate out of the streaming parser
for idx, candidate in enumerate(load_candidates("data/candidates.jsonl")):
    
    # Run your feature extractor method
    extracted_features = extractor.extract(candidate)
    
    print(f"=== TEST CANDIDATE {idx + 1} EXTRACTED FEATURES ===")
    pprint(extracted_features)
    print("=" * 50 + "\n")
    
    # Stop after inspecting 2 candidates to verify the data shapes look right
    if idx == 1:
        break