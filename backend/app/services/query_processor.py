import re


class QueryProcessor:

    def clean(self, query: str):
        query = query.lower()
        query = re.sub(r"[^\w\s]", "", query)
        return query.strip()

    def expand(self, query: str):
        """
        Simple expansion (can upgrade later with LLM/HyDE)
        """
        synonyms = {
            "ml": "machine learning",
            "ai": "artificial intelligence",
            "nlp": "natural language processing"
        }

        for key, val in synonyms.items():
            if key in query:
                query += " " + val

        return query
    
    def classify(self, query: str):
        q = query.lower().strip()

        greetings = ["hi", "hello", "hey", "how are you", "good morning", "good evening"]

        if any(g in q for g in greetings):
            return "chat"

        if len(q.split()) <= 2:
            return "chat"  

        return "rag"