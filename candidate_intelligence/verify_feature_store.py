import pandas as pd

df = pd.read_parquet("output/candidate_features.parquet")

print("=" * 60)
print("Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nFirst 5 rows")
print(df.head())

print("\nNull values")
print(df.isnull().sum().sort_values(ascending=False).head(20))

print("\nMemory Usage")
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")