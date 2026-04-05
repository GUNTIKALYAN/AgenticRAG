import requests
import os


class EmbeddingService:

    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/embeddings"
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise Exception("OPENROUTER_API_KEY missing")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def embed_query(self, text):
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={
                "model": "text-embedding-3-small",
                "input": text
            }
        )

        if response.status_code != 200:
            print("Embedding API error:", response.text)
            raise Exception("Embedding API failed")

        data = response.json()

        return data["data"][0]["embedding"]

    def embed_texts(self, texts):
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={
                "model": "text-embedding-3-small",
                "input": texts
            }
        )

        if response.status_code != 200:
            print("Embedding API error:", response.text)
            raise Exception("Embedding API failed")

        data = response.json()

        return [item["embedding"] for item in data["data"]]