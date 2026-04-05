# import faiss
# import numpy as np
# import os


# class FAISSStore:

#     def __init__(self, dim: int, index_path: str):
#         self.dim = dim
#         self.index_path = index_path

#         self.index = self._load_or_create()

#     def _load_or_create(self):

#         if os.path.exists(self.index_path):
#             print("Loading existing FAISS index...")
#             return faiss.read_index(self.index_path)

#         print("Creating new FAISS index...")
#         return faiss.IndexFlatIP(self.dim)

#     def _normalize(self, vectors):
#         return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

#     def add(self, vectors):
#         vectors = np.array(vectors).astype("float32")
#         vectors = self._normalize(vectors)

#         self.index.add(vectors)
#         print(f"Total vectors: {self.index.ntotal}")

#     def search(self, query_vector, k=5):
#         query_vector = np.array([query_vector]).astype("float32")
#         query_vector = self._normalize(query_vector)

#         scores, indices = self.index.search(query_vector, k)

#         return scores[0], indices[0]

#     def save(self):
#         faiss.write_index(self.index, self.index_path)

import faiss
import numpy as np
import os


class FAISSStore:

    def __init__(self, dim: int, index_path: str):
        self.dim = dim
        self.index_path = index_path
        os.makedirs(os.path.dirname(index_path), exist_ok=True)


        self.index = self._load_or_create()

    def _load_or_create(self):

        if os.path.exists(self.index_path):
            print("Loading existing FAISS index...")
            index = faiss.read_index(self.index_path)

            # ✅ Safety check (you didn’t have this)
            if index.d != self.dim:
                raise ValueError(
                    f"FAISS dimension mismatch! Expected {self.dim}, got {index.d}"
                )

            return index

        print("Creating new FAISS index...")
        return faiss.IndexFlatIP(self.dim)

    def _normalize(self, vectors):
        norm = np.linalg.norm(vectors, axis=1, keepdims=True)
        norm[norm == 0] = 1
        return vectors / norm
    
    def add(self, vectors):
        vectors = np.array(vectors).astype("float32")

        # ✅ Dimension validation
        if vectors.shape[1] != self.dim:
            raise ValueError(
                f"Embedding dimension mismatch! Expected {self.dim}, got {vectors.shape[1]}"
            )

        vectors = self._normalize(vectors)

        self.index.add(vectors)
        self.save()

        print(f"Total vectors: {self.index.ntotal}")

    def search(self, query_vector, k=5):

        if self.index.ntotal == 0:
            print("FAISS index is empty")
            return [], []
        
        query_vector = np.array([query_vector]).astype("float32")

        if query_vector.shape[1] != self.dim:
            raise ValueError(
                f"Query dimension mismatch! Expected {self.dim}, got {query_vector.shape[1]}"
            )

        query_vector = self._normalize(query_vector)

        scores, indices = self.index.search(query_vector, k)
        
        return scores[0], indices[0]

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)