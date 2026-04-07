from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.dependencies.cache import init_cache
from app.services.rerank_service import RerankService
from app.dependencies.model_loader import get_embedding_config
from app.db.faiss_store import FAISSStore
from app.db.metadata_store import MetadataStore
from app.services.hybrid_search_service import HybridSearchService
from app.core.config import settings

class AppState:
    cache = None
    reranker = None
    faiss = None
    metadata = None
    hybrid = None


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
        dim=settings.EMBEDDING_DIM,
        index_path=settings.FAISS_INDEX_PATH
    )

    state.metadata = MetadataStore(settings.METADATA_PATH)
    print(f"Metadata loaded at startup: {len(state.metadata.data)}")

    # HYBRID BM25
    state.hybrid = HybridSearchService(state.metadata)

    print("Startup Complete")

    yield

    print("Shutting down system...")