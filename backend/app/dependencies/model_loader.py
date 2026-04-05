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