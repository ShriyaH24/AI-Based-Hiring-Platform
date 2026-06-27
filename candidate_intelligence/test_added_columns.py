import pandas as pd

df = pd.read_parquet("output/candidate_features.parquet")

print(df.columns.tolist())