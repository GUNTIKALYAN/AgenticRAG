class ContextBuilder:

    def build(self, docs, max_chars=3000):

        context_parts = []
        sources = []
        total_length = 0

        for doc in docs:
            metadata = doc.get("metadata", {})
            text = metadata.get("text", "")
            source = metadata.get("source", "unknown")

            if not text:
                continue

            # Stop if too long
            if total_length + len(text) > max_chars:
                break

            context_parts.append(f"[Source: {source}]\n{text}")
            sources.append(source)

            total_length += len(text)

        context = "\n\n".join(context_parts)

        return context, list(set(sources))