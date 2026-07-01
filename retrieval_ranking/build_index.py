import numpy as np
import faiss

# load embeddings
embeddings = np.load("data/candidate_embeddings.npy")

# normalize (important for cosine similarity)
faiss.normalize_L2(embeddings)

dim = embeddings.shape[1]

# FAISS index
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

# save index
faiss.write_index(index, "data/faiss.index")

print("FAISS index built with:", index.ntotal, "candidates")