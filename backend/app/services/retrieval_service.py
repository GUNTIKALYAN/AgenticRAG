from app.db.faiss_store import FAISSStore
from app.db.metadata_store import MetadataStore
from app.services.embedding_service import EmbeddingService
from app.services.hybrid_search_service import HybridSearchService
from app.core.config import settings

import numpy as np


class RetrievalService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.vector_store = FAISSStore(
            dim=384,
            index_path=settings.FAISS_INDEX_PATH
        )

        self.metadata_store = MetadataStore(settings.METADATA_PATH)

        # Hybrid search
        self.hybrid = HybridSearchService(self.metadata_store)

        self.similarity_threshold = 0.25

    def retrieve(self, query: str, k: int = 10, allowed_sources=None):

        #  1. Semantic Search 
        query_vector = self.embedder.embed_query(query)

        faiss_scores, faiss_indices = self.vector_store.search(query_vector, k)

        faiss_indices = np.atleast_1d(faiss_indices)
        faiss_scores = np.atleast_1d(faiss_scores)

        if faiss_indices.ndim == 2:
            faiss_indices = faiss_indices[0]
            faiss_scores = faiss_scores[0]

        semantic_results = {}

        for idx, score in zip(faiss_indices, faiss_scores):

            if score < 0.2:
                continue

            if idx == -1:
                continue

            if score < self.similarity_threshold:
                continue

            semantic_results[int(idx)] = float(score)

        #  2. Keyword Search 
        keyword_results = self.hybrid.keyword_search(query, k)

        keyword_scores = {
            item["index"]: item["score"] for item in keyword_results
        }

        #  3. Merge 
        combined = {}

        for idx, score in semantic_results.items():
            combined[idx] = score * 0.7  

        for idx, score in keyword_scores.items():
            if idx in combined:
                combined[idx] += score * 0.3
            else:
                combined[idx] = score * 0.3

        #  4. Sort 
        sorted_indices = sorted(
            combined.keys(),
            key=lambda x: combined[x],
            reverse=True
        )[:k]

        #  5. Build Results 
        results = []

        for idx in sorted_indices:
            metadata = self.metadata_store.get(idx)

            if metadata:
                results.append({
                    "score": combined[idx],
                    "metadata": metadata
                })

        #  6. Fallback 
        if not results:
            print("⚠️ Hybrid fallback triggered")

            for idx in list(combined.keys())[:3]:
                metadata = self.metadata_store.get(idx)

                if metadata:
                    results.append({
                        "score": combined[idx],
                        "metadata": metadata
                    })

        return results