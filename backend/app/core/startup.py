from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.dependencies.model_loader import load_embedding_model
from app.dependencies.cache import init_cache
from app.services.rerank_service import RerankService


class AppState:
    embedding_model = None
    cache = None
    reranker = None


state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up Agentic RAG system...")

    # Load embedding model
    state.embedding_model = load_embedding_model()

    # Cache
    state.cache = init_cache()

    # Reranker (safe load)
    state.reranker = RerankService()

    print(f"Cache initialized: {state.cache is not None}")
    print(f"Reranker loaded: {state.reranker is not None}")

    print("Startup Complete")

    yield

    print("Shutting down system...")