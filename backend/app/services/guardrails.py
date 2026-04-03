class Guardrails:

    def validate_input(self, query: str):
        if not query or len(query.strip()) == 0:
            return False, "Empty query"

        if len(query) > 1000:
            return False, "Query too long"

        # Basic injection protection
        blocked_phrases = ["ignore previous", "system prompt", "override"]

        for phrase in blocked_phrases:
            if phrase in query.lower():
                return False, "Unsafe query detected"

        return True, None

    def validate_output(self, response: str):
        if not response or len(response.strip()) == 0:
            return "No response generated"

        # Simple hallucination fallback
        if "i don't know" in response.lower():
            return "I don't have enough information from the documents."

        return response