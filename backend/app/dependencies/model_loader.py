from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model = None

def load_embedding_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        print("Embedding model loaded")

    return _model