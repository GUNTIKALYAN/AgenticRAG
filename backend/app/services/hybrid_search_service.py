from rank_bm25 import BM25Okapi


class HybridSearchService:

    def __init__(self, metadata_store):
        self.metadata_store = metadata_store

        corpus = [
            item["text"] for item in metadata_store.data
            if item.get("text")
        ]

        if len(corpus) == 0:
            print("⚠️ Empty corpus — BM25 disabled")
            self.bm25 = None
            self.tokenized_corpus = []
            return

        self.tokenized_corpus = [doc.split() for doc in corpus]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def keyword_search(self, query, k=5):

        if self.bm25 is None:
            return []

        tokens = query.split()
        scores = self.bm25.get_scores(tokens)

        results = []

        for i, score in enumerate(scores):
            results.append({
                "index": i,
                "score": float(score)
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return results[:k]