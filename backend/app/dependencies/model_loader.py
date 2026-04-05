# from sentence_transformers import SentenceTransformer
# from app.core.config import settings

# _model = None

# def load_embedding_model():
#     global _model

#     if _model is None:
#         print("Loading embedding model...")
#         _model = SentenceTransformer(settings.EMBEDDING_MODEL)
#         print("Embedding model loaded")

#     return _model

from app.core.config import settings


def get_embedding_config():
    """
    Returns embedding configuration for OpenRouter/OpenAI
    """

    return {
        "api_key": settings.OPENROUTER_API_KEY,
        "model": settings.EMBEDDING_MODEL,
        "base_url": "https://openrouter.ai/api/v1"
    }