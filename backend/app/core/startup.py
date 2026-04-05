# from contextlib import asynccontextmanager
# from fastapi import FastAPI

# from app.dependencies.model_loader import load_embedding_model
# from app.dependencies.cache import init_cache
# from app.services.rerank_service import RerankService


# class AppState:
#     embedding_model = None
#     cache = None
#     reranker = None


# state = AppState()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Starting up Agentic RAG system...")

#     # Load embedding model
#     state.embedding_model = None

#     # Cache
#     state.cache = init_cache()

#     # Reranker 
#     state.reranker = None

#     print(f"Cache initialized: {state.cache is not None}")
#     print(f"Reranker loaded: {state.reranker is not None}")

#     print("Startup Complete")

#     yield

#     print("Shutting down system...")

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.dependencies.cache import init_cache
from app.services.rerank_service import RerankService


class AppState:
    cache = None
    reranker = None


state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up Agentic RAG system...")

    # ❌ REMOVE embedding model loading

    # Cache
    state.cache = init_cache()

    # Reranker
    state.reranker = RerankService()

    print(f"Cache initialized: {state.cache is not None}")
    print(f"Reranker loaded: {state.reranker is not None}")

    print("Startup Complete")

    yield

    print("Shutting down system...")