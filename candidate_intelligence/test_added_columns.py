import os
import pandas as pd

REQUIRED_COLUMNS = ["cri_score", "skill_evidence_score", "growth_potential_score"]
PARQUET_PATH = "output/candidate_features.parquet"

assert os.path.exists(PARQUET_PATH), f"Feature store not found at {PARQUET_PATH}"

df = pd.read_parquet(PARQUET_PATH)

print(df.columns.tolist())

for column in REQUIRED_COLUMNS:
    print(f"{column}: {column in df.columns}")

for column in REQUIRED_COLUMNS:
    assert column in df.columns, f"Column {column} is missing"
    assert df[column].notna().all(), f"Column {column} contains null values"
    assert ((df[column] >= 0) & (df[column] <= 100)).all(), f"Column {column} has invalid range"
