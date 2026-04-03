from app.services.llm_service import LLMService


class HyDEService:

    def __init__(self):
        self.llm = LLMService()

    def generate_hypothetical_doc(self, query: str):

        prompt = f"""
Write a detailed answer paragraph for the question below.
This is ONLY for retrieval improvement.

Question:
{query}

Answer:
"""

        return self.llm.generate(query, prompt)