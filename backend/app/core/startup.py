from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.dependencies.cache import init_cache
from app.services.rerank_service import RerankService
from app.dependencies.model_loader import get_embedding_config
from app.db.faiss_store import FAISSStore
from app.core.config import settings

class AppState:
    cache = None
    reranker = None


state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up Agentic RAG system...")

    state.embedding_model = get_embedding_config()


    # Cache
    state.cache = init_cache()

    # Reranker
    state.reranker = RerankService()

    state.faiss = FAISSStore(
        dim=1536,
        index_path=settings.FAISS_INDEX_PATH
    )

    print(f"Cache initialized: {state.cache is not None}")
    print(f"Reranker loaded: {state.reranker is not None}")

    print("Startup Complete")

    yield

    print("Shutting down system...")