class ContextBuilder:

    def build(self, docs, max_chars=2000):

        # take only top 3 docs
        docs = docs[:3]

        context_parts = []
        sources = []

        for doc in docs:
            metadata = doc.get("metadata", {})
            text = metadata.get("text", "").strip()
            source = metadata.get("source", "unknown")

            if not text:
                continue

            context_parts.append(f"{text}")
            sources.append(source)

        context = "\n\n".join(context_parts)

        return context, list(set(sources))