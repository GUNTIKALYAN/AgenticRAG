import faiss
import numpy as np
import os


class FAISSStore:

    def __init__(self, dim: int, index_path: str):
        self.dim = dim
        self.index_path = index_path

        self.index = self._load_or_create()

    # def _load_or_create(self):

    #     os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

    #     if os.path.exists(self.index_path):
    #         print("✅ Loading existing FAISS index")
    #         return faiss.read_index(self.index_path)

    #     print("🆕 Creating new FAISS index")
    #     return faiss.IndexFlatIP(self.dim)  # cosine similarity
    def _load_or_create(self):

        if os.path.exists(self.index_path):
            print("🔹 Loading existing FAISS index...")
            return faiss.read_index(self.index_path)

        print("🔹 Creating new FAISS index...")
        return faiss.IndexFlatIP(self.dim)

    def _normalize(self, vectors):
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    def add(self, vectors):
        vectors = np.array(vectors).astype("float32")
        vectors = self._normalize(vectors)

        self.index.add(vectors)
        print(f"📦 Total vectors: {self.index.ntotal}")

    def search(self, query_vector, k=5):
        query_vector = np.array([query_vector]).astype("float32")
        query_vector = self._normalize(query_vector)

        scores, indices = self.index.search(query_vector, k)

        return scores[0], indices[0]

    def save(self):
        faiss.write_index(self.index, self.index_path)