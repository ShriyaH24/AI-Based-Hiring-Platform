import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pandas as pd

# load dataset
df = pd.read_parquet("data/candidate_features.parquet")

# load FAISS index
index = faiss.read_index("data/faiss.index")

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_candidates(job_description, top_k=100):

    # convert job description → embedding
    query_vec = model.encode([job_description])

    # normalize for cosine similarity
    faiss.normalize_L2(query_vec)

    # search in FAISS
    scores, indices = index.search(query_vec, top_k)

    # get matched rows
    results = df.iloc[indices[0]].copy()

    # add similarity score
    results["score"] = scores[0]

    # return selected columns (clean output)
    return results[[
        "candidate_id",
        "headline",
        "summary",
        "skills",
        "score"
    ]]


if __name__ == "__main__":

    jd = "Looking for backend engineer with Python, Spark and AWS experience"

    results = search_candidates(jd)

    print("\nTop Candidates:\n")
    print(results)

    # SAVE OUTPUT TO CSV (what your friend needs)
    results.to_csv("retrieved_candidates.csv", index=False)

    print("\nSaved as retrieved_candidates.csv")