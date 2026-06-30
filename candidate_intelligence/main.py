import json
import os
import pandas as pd

from parser import load_candidates
from validator import CandidateValidator
from feature_extractor import FeatureExtractor
from behavioral_engine import BehavioralEngine
from candidate_readiness import CandidateReadinessIndex
from skill_evidence import SkillEvidence
from growth_potential import GrowthPotential

# File System Configurations
SCHEMA_PATH = "data/candidate_schema.json"
DATASET_PATH = "data/candidates.jsonl"
PARQUET_OUTPUT = "output/candidate_features.parquet"

def run_production_pipeline():
    print("=" * 70)
    print("   RUNNING CANDIDATE INTELLIGENCE PIPELINE & INTEGRITY AUDIT")
    print("=" * 70)

    # 1. Initialize Modules
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    validator = CandidateValidator(schema)
    extractor = FeatureExtractor()
    behavior_engine = BehavioralEngine()
    readiness_engine = CandidateReadinessIndex()
    skill_evidence_engine = SkillEvidence()
    growth_engine = GrowthPotential()
    
    records = []
    
    # 2. Extract Data Matrix Streams
    print(f"\n[1/3] Streaming and processing rows from {DATASET_PATH}...")
    for candidate in load_candidates(DATASET_PATH):
        # Validate against original json schema rules
        validator.validate_candidate(candidate)
        
        # Pull structural and textual features
        profile_and_skills = extractor.extract(candidate)
        
        # Pull transactional behavioral elements
        behavioral_metrics = behavior_engine.extract(candidate)
        
        # STEP 6: Combine all matrices into one flattened dictionary
        unified_record = {**profile_and_skills, **behavioral_metrics}
        readiness_metrics = readiness_engine.extract(unified_record)
        skill_evidence_metrics = skill_evidence_engine.extract(unified_record)
        growth_metrics = growth_engine.extract(unified_record)
        unified_record.update(readiness_metrics)
        unified_record.update(skill_evidence_metrics)
        unified_record.update(growth_metrics)
        records.append(unified_record)
        
    # 3. Save Matrix Dataset to Parquet
    print(f"\n[2/3] Compiling and exporting database rows ({len(records)} entries)...")
    df = pd.DataFrame(records)
    
    os.makedirs(os.path.dirname(PARQUET_OUTPUT), exist_ok=True)
    df.to_parquet(PARQUET_OUTPUT, index=False, compression="snappy")
    print(f" -> SUCCESS: Feature store saved to '{PARQUET_OUTPUT}'")
    
    # 4. STEP 7: Comprehensive Final Quality Control Checks
    print("\n[3/3] Executing downstream pipeline data audit check...")
    print("-" * 70)
    
    audit_passed = True
    
    # Check A: Row Count Check
    print(f" -> Total processed rows compiled: {len(df)}")
    if len(df) != 100000:
        audit_passed = False
        print(" -> WARNING: Expected 100000 rows but found {}".format(len(df)))
    
    # Check B: Key Duplication Test
    duplicates = df.duplicated(subset=["candidate_id"]).sum()
    print(f" -> Duplicate candidate identifiers: {duplicates}")
    if duplicates > 0:
        audit_passed = False
    
    # Check C: Empty Document Search Check
    empty_docs = (df["search_document"].str.strip().str.len() == 0).sum()
    print(f" -> Blank search document fields: {empty_docs}")
    if empty_docs > 0:
        audit_passed = False
        
    # Check D: Logical Range Boundary Check
    negative_experience = (df["years_of_experience"] < 0).sum()
    print(f" -> Anomalous negative experience entries: {negative_experience}")
    if negative_experience > 0:
        audit_passed = False

    # Check E: New scoring columns presence and bounds
    required_score_columns = ["cri_score", "skill_evidence_score", "growth_potential_score"]
    missing_score_columns = [col for col in required_score_columns if col not in df.columns]
    if missing_score_columns:
        audit_passed = False
        print(f" -> Missing new scoring columns: {missing_score_columns}")
    else:
        null_score_values = df[required_score_columns].isnull().any().any()
        score_range_errors = (
            ((df[required_score_columns] < 0) | (df[required_score_columns] > 100)).any().any()
        )
        print(f" -> New scoring columns contain nulls: {null_score_values}")
        print(f" -> New scoring columns outside 0-100 range: {score_range_errors}")
        if null_score_values or score_range_errors:
            audit_passed = False

    print("-" * 70)
    if audit_passed:
        print(" AUDIT LOG STATUS: PASSED. Feature vectors match compliance rules.")
    else:
        print(" AUDIT LOG STATUS: FAILED. Check file input streams for corrupt schema records.")
    print("=" * 70)

if __name__ == "__main__":
    run_production_pipeline()