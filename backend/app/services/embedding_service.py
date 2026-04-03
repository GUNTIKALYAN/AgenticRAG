from app.dependencies.model_loader import load_embedding_model

class EmbeddingService:

    def __init__(self):
        self.model = load_embedding_model()

    def embed_texts(self, texts):
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query):
        return self.model.encode([query])[0]