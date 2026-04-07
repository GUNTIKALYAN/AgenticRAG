import numpy as np

from app.services.embedding_service import EmbeddingService
from app.core.config import settings
from app.core.startup import state

from app.db.faiss_store import FAISSStore
from app.db.metadata_store import MetadataStore
from app.services.hybrid_search_service import HybridSearchService


class RetrievalService:

    def __init__(self):

        self.embedder = EmbeddingService()

        #  FAISS LOAD
        if state.faiss is None:
            print("⚠️ FAISS missing → loading from disk")
            state.faiss = FAISSStore(
                dim=settings.EMBEDDING_DIM,
                index_path=settings.FAISS_INDEX_PATH
            )

        self.vector_store = state.faiss

        # METADATA LOAD
        if state.metadata is None:
            print("⚠️ Metadata missing → loading from disk")
            state.metadata = MetadataStore(settings.METADATA_PATH)

        self.metadata_store = state.metadata

        # HYBRID
        if state.hybrid is None:
            state.hybrid = HybridSearchService(self.metadata_store)

        self.hybrid = state.hybrid

        self.similarity_threshold = 0.25


    def retrieve(self, query: str, k: int = 10, allowed_sources=None):

        # reload metadata every query
        if state.metadata is None:
            print("Metadata None at query  reloading")
            state.metadata = MetadataStore(settings.METADATA_PATH)

        self.metadata_store = state.metadata

        print(f"Metadata available: {len(self.metadata_store.data)}")

        # rebuild BM25
        self.hybrid = HybridSearchService(self.metadata_store)
        state.hybrid = self.hybrid

        if self.vector_store.index.ntotal == 0:
            print("FAISS empty → reloading from disk")

            from app.db.faiss_store import FAISSStore
            from app.core.config import settings

            self.vector_store = FAISSStore(
                dim=settings.EMBEDDING_DIM,
                index_path=settings.FAISS_INDEX_PATH
            )

        # SAFETY CHECKS
        if self.vector_store is None:
            print("FAISS not initialized")
            return []

        if self.metadata_store is None or not hasattr(self.metadata_store, "data"):
            print("Metadata invalid")
            return []

        # 1. Semantic Search (FAISS)
        query_vector = self.embedder.embed_query(query)

        faiss_scores, faiss_indices = self.vector_store.search(query_vector, k)

        faiss_indices = np.atleast_1d(faiss_indices)
        faiss_scores = np.atleast_1d(faiss_scores)

        semantic_results = {}

        for idx, score in zip(faiss_indices, faiss_scores):

            if idx == -1:
                continue

            if score < self.similarity_threshold:
                continue

            semantic_results[int(idx)] = float(score)

        # 2. Keyword Search (BM25)
        keyword_results = self.hybrid.keyword_search(query, k)

        keyword_scores = {
            item["index"]: item["score"] for item in keyword_results
        }

        # 3. Merge Scores
        combined = {}

        for idx, score in semantic_results.items():
            combined[idx] = score * 0.7

        for idx, score in keyword_scores.items():
            if idx in combined:
                combined[idx] += score * 0.3
            else:
                combined[idx] = score * 0.3

        # 4. Sort
        sorted_indices = sorted(
            combined.keys(),
            key=lambda x: combined[x],
            reverse=True
        )[:k]

        # 5. Build Results
        results = []
        bad_keywords = [
            "declaration",
            "instructions",
            "signature",
            "photo",
            "thumb impression"
        ]

        for idx in sorted_indices:
            metadata = self.metadata_store.get(idx)
            
            if not metadata:
                continue

            text = metadata.get("text", "").lower()

            # skip noisy chunks
            if any(k in text for k in bad_keywords):
                continue

            results.append({
                "score": combined[idx],
                "metadata": metadata
            })
            # if metadata:
            #     results.append({
            #         "score": combined[idx],
            #         "metadata": metadata
            #     })

        # 6. Fallback
        if not results:
            print("Hybrid fallback triggered")

            for idx in list(combined.keys())[:3]:
                metadata = self.metadata_store.get(idx)

                if metadata:
                    results.append({
                        "score": combined[idx],
                        "metadata": metadata
                    })

        return results