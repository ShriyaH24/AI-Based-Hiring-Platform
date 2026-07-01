import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# load data
df = pd.read_parquet("data/candidate_features.parquet")

# safe string conversion
df["headline"] = df["headline"].astype(str)
df["summary"] = df["summary"].astype(str)
df["search_document"] = df["search_document"].astype(str)

# FIX: skills is list → convert safely
df["skills"] = df["skills"].apply(
    lambda x: " ".join(x) if isinstance(x, list) else str(x)
)

# final text
df["final_text"] = (
    df["headline"] + " " +
    df["summary"] + " " +
    df["skills"] + " " +
    df["search_document"]
)

print("Sample text:", df["final_text"].iloc[0])

# model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = df["final_text"].tolist()

# embeddings
embeddings = model.encode(texts, show_progress_bar=True)

print("Shape:", embeddings.shape)

# SAVE embeddings (IMPORTANT)
np.save("data/candidate_embeddings.npy", embeddings)

print("Saved embeddings successfully")