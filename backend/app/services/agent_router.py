from app.services.retrieval_service import RetrievalService
from app.services.query_processor import QueryProcessor
from app.services.cache_service import CacheService
from app.services.llm_service import LLMService
from app.services.guardrails import Guardrails
from app.core.startup import state
from app.services.context_builder import ContextBuilder
from app.services.hyde_service import HyDEService

import numpy as np

class AgentRouter:

    def __init__(self):
        self.retriever = RetrievalService()
        self.reranker = state.reranker
        self.processor = QueryProcessor()
        self.cache = CacheService(state.cache)
        self.llm = LLMService()
        self.guardrails = Guardrails()
        self.context_builder = ContextBuilder()
        self.hyde = HyDEService()
        self.current_docs = None

    def handle_query(self, query: str):

        # 1. Guardrails
        valid, error = self.guardrails.validate_input(query)
        if not valid:
            return {"answer": error, "sources": [], "confidence": 0.0}

        # 2. Clean + Expand
        clean_query = self.processor.clean(query)
        expanded_query = self.hyde.generate_hypothetical_doc(clean_query)

        query_type = self.processor.classify(clean_query)

        if query_type == "chat":
            return {
                "answer": self.llm.general_chat(clean_query),
                "sources": []
            }
        self.current_docs = "latest"
        
        # 3. Cache
        cached = self.cache.get(expanded_query)
        if cached:
            return cached

        # 4. Retrieve
        retrieved_docs = self.retriever.retrieve(expanded_query, k=10)

        if not retrieved_docs:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
            }
        print("Retrieved docs:",retrieved_docs)
        print("Using reranker:",bool(self.reranker))
        # 5. Rerank
        if self.reranker:
            top_docs = self.reranker.rerank(expanded_query, retrieved_docs)
        else:
            top_docs = sorted(retrieved_docs, key=lambda x: x.get("score") if x.get("score") is not None else -1,reverse=True)[:5]  # fallback

        # 6. Context Optimization
        context, sources = self.context_builder.build(top_docs)

        if not context:
            return {
                "answer": "No usable context found.",
                "sources": [],
            }

        # 7. LLM
        answer = self.llm.generate(clean_query, context)

        # 8. Guardrails output
        answer = self.guardrails.validate_output(answer)

    
        result = {
            "answer": answer,
            "sources": sources,
        }

        # 10. Cache
        self.cache.set(expanded_query, result)

        return result