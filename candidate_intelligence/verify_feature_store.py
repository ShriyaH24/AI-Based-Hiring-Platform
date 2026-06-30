import pandas as pd

REQUIRED_COLUMNS = [
    "cri_score",
    "skill_evidence_score",
    "growth_potential_score",
]


df = pd.read_parquet("output/candidate_features.parquet")

assert len(df) == 100000, f"Expected 100000 rows, found {len(df)}"
assert df.duplicated(subset=["candidate_id"]).sum() == 0, "Duplicate candidate IDs detected"

print("=" * 60)
print("Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nRequired columns present")
for column in REQUIRED_COLUMNS:
    print(f"- {column}: {column in df.columns}")

print("\nNull values")
nulls = df.isnull().sum().sort_values(ascending=False)
print(nulls[nulls > 0].head(20))

print("\nScore ranges")
for column in REQUIRED_COLUMNS:
    print(f"- {column}: [{df[column].min():.2f}, {df[column].max():.2f}]")
    assert df[column].notna().all(), f"{column} contains null values"
    assert ((df[column] >= 0) & (df[column] <= 100)).all(), f"{column} has values outside the 0-100 range"

print("\nRow count")
print(len(df))

print("\nDuplicate candidate IDs")
print(df.duplicated(subset=["candidate_id"]).sum())

print("\nMemory Usage")
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")