# # from sentence_transformers import CrossEncoder


# # class RerankService:

# #     def __init__(self):
# #         print("🔹 Loading reranker model...")
# #         try:
# #             self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
# #         except Exception as e:
# #             print(f"❌ Reranker failed to load: {e}")
# #             self.model = None

# #     def rerank(self, query, docs):

# #         # 🔒 Fallback if model not loaded
# #         if self.model is None:
# #             return docs[:3]

# #         # 🔒 Safe text extraction
# #         pairs = []
# #         valid_docs = []

# #         for doc in docs:
# #             text = doc.get("metadata", {}).get("text")

# #             if text:
# #                 pairs.append((query, text))
# #                 valid_docs.append(doc)

# #         if not pairs:
# #             return docs[:3]

# #         scores = self.model.predict(pairs)

# #         for i, score in enumerate(scores):
# #             valid_docs[i]["rerank_score"] = float(score)

# #         # Sort by rerank score
# #         valid_docs = sorted(
# #             valid_docs,
# #             key=lambda x: x["rerank_score"],
# #             reverse=True
# #         )

# #         return valid_docs[:3]


# from sentence_transformers import CrossEncoder


# class RerankService:

#     def __init__(self):
#         print("🔹 Loading reranker model...")
#         try:
#             self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
#         except Exception as e:
#             print(f"❌ Reranker failed: {e}")
#             self.model = None

#     def rerank(self, query, docs):

#         if not docs:
#             return []

#         # 🔒 If model not available → fallback
#         if self.model is None:
#             for doc in docs:
#                 doc["rerank_score"] = doc.get("score", 0.1)
#             return docs[:3]

#         pairs = []
#         valid_indices = []

#         for i, doc in enumerate(docs):
#             text = doc.get("metadata", {}).get("text")

#             if text:
#                 pairs.append((query, text))
#                 valid_indices.append(i)

#         # 🔒 If no valid text → fallback
#         if not pairs:
#             for doc in docs:
#                 doc["rerank_score"] = doc.get("score", 0.1)
#             return docs[:3]

#         scores = self.model.predict(pairs)

#         # 🔥 Assign scores properly
#         for idx, score in zip(valid_indices, scores):
#             docs[idx]["rerank_score"] = float(score)

#         # 🔥 Ensure ALL docs have score
#         for doc in docs:
#             if "rerank_score" not in doc:
#                 doc["rerank_score"] = doc.get("score", 0.1)

#         # Sort
#         docs = sorted(docs, key=lambda x: x["rerank_score"], reverse=True)

#         return docs[:3]


from sentence_transformers import CrossEncoder
import numpy as np


class RerankService:

    def __init__(self):
        print("🔹 Loading reranker model...")
        try:
            self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        except Exception as e:
            print(f"❌ Reranker failed: {e}")
            self.model = None

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def rerank(self, query, docs):

        if not docs:
            return []

        # 🔒 fallback
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

        # 🔒 fallback if no valid text
        if not pairs:
            for doc in docs:
                doc["rerank_score"] = doc.get("score", 0.1)
            return docs[:3]

        # 🔥 RAW logits
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