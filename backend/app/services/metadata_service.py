import time


def create_metadata(doc, chunk_id,chunk_text):
    return {
        "source": doc["source"],
        "chunk_id": chunk_id,
        "text": chunk_text,
        "timestamp": time.time(),
        "length": len(chunk_text)
    }