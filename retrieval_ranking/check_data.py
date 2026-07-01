import pandas as pd

df = pd.read_parquet("data/candidate_features.parquet")

print("Shape:", df.shape)
print("Columns:", df.columns)
print(df.head())