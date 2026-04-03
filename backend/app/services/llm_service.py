import requests
from app.core.config import settings


class LLMService:

    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def _build_prompt(self, query: str, context: str) -> str:

        return f"""
You are a highly accurate AI assistant.

STRICT RULES:
1. Answer ONLY using the provided context
2. If answer is not clearly present → say "I don't know"
3. Do NOT assume or add external knowledge
4. Be precise and concise
5. Cite sources using [Source: filename] at the ned line of response

RESPONSE STYLE:
- Give a clear explanation (2–4 sentences)
- Be specific, not generic
- Cite sources using [Source: filename] at end line of response


CONTEXT:
{context}

QUESTION:
{query}

FINAL ANSWER:
"""

    def generate(self, query: str, context: str):

        prompt = self._build_prompt(query, context)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,   
            "max_tokens": 400
        }

        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code != 200:
            return "LLM Error"

        return response.json()["choices"][0]["message"]["content"]
    
    def general_chat(self, query: str):

        prompt = f"""
    You are a friendly AI assistant.

    - Respond naturally like ChatGPT
    - Be helpful and conversational
    - No need to use any document context

    User: {query}
    Assistant:
    """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code != 200:
            return "Hello! How can I help you?"

        data = response.json()
        return data["choices"][0]["message"]["content"]