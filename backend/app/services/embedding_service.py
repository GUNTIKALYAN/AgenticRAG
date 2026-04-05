# # from app.dependencies.model_loader import load_embedding_model

# # class EmbeddingService:

# #     def __init__(self):
# #         self.model = load_embedding_model()

# #     def embed_texts(self, texts):
# #         return self.model.encode(texts, show_progress_bar=True)

# #     def embed_query(self, query):
# #         return self.model.encode([query])[0]

# from openai import OpenAI
# import os


# class EmbeddingService:

#     def __init__(self):
#         self.client = OpenAI(
#             base_url="https://openrouter.ai/api/v1",
#             api_key=os.getenv("OPENROUTER_API_KEY"),
#         )
#         self.model = "text-embedding-3-small"

#     def embed_texts(self, texts):
#         response = self.client.embeddings.create(
#             model=self.model,
#             input=texts
#         )
#         return [item.embedding for item in response.data]

#     def embed_query(self, query):
#         response = self.client.embeddings.create(
#             model=self.model,
#             input=query
#         )
#         return response.data[0].embedding

import requests
import time
from app.dependencies.model_loader import get_embedding_config


class EmbeddingService:

    def __init__(self):
        config = get_embedding_config()
        self.api_key = config["api_key"]
        self.model = config["model"]
        self.url = f"{config['base_url']}/embeddings"

    def _request(self, input_data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "input": input_data
        }

        # ✅ retry logic (you didn’t have this before)
        for attempt in range(3):
            try:
                response = requests.post(self.url, json=payload, headers=headers, timeout=30)

                if response.status_code == 200:
                    return response.json()["data"]

                print(f"Embedding API error: {response.text}")

            except Exception as e:
                print(f"Embedding request failed: {e}")

            time.sleep(2 ** attempt)

        raise Exception("Embedding API failed after retries")

    def embed_texts(self, texts):
        """
        Batch embedding (IMPORTANT for cost + speed)
        """
        data = self._request(texts)
        return [item["embedding"] for item in data]

    def embed_query(self, query):
        data = self._request([query])
        return data[0]["embedding"]