from sentence_transformers import CrossEncoder
import numpy as np


class RerankService:

    def __init__(self):
        print("Loading reranker model...")
        try:
            self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        except Exception as e:
            print(f"Reranker failed: {e}")
            self.model = None

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def rerank(self, query, docs):

        if not docs:
            return []

        # fallback
        if self.model is None:
            for doc in docs:
                doc["rerank_score"] = doc.get("score", 0.1)
            return docs[:3]

        pairs = []
        valid_indices = []

        for i, doc in enumerate(docs):
            text = doc.get("metadata", {}).get("text")

            if text and len(text.strip()) > 10:
                pairs.append((query, text))
                valid_indices.append(i)

        # fallback if no valid text
        if not pairs:
            for doc in docs:
                doc["rerank_score"] = doc.get("score", 0.1)
            return docs[:3]

        # RAW logits
        scores = self.model.predict(pairs)
        print("Raw Scores:",scores)

        # Assign scores
        for idx, score in zip(valid_indices, scores):
            docs[idx]["rerank_score"] = float(score)

        # Ensure all docs have score
        for doc in docs:
            if "rerank_score" not in doc:
                doc["rerank_score"] = 0.1

        # Sort
        docs = sorted(
            docs,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return docs[:3]