# import os
# import json
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# from app.utils.helpers import load_documents
# from app.services.embedding_service import EmbeddingService
# from app.services.metadata_service import create_metadata
# from app.db.faiss_store import FAISSStore
# from app.db.metadata_store import MetadataStore

# # Paths (production-safe)
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# DATA_DIR = os.path.join(BASE_DIR, "data")
# RAW_DOCS_PATH = os.path.join(DATA_DIR, "raw_docs")
# FAISS_PATH = os.path.join(DATA_DIR, "faiss", "index.bin")
# METADATA_PATH = os.path.join(DATA_DIR, "metadata", "metadata.json")
# CHUNKS_PATH = os.path.join(DATA_DIR, "processed", "chunks.json")



# def run_ingestion():
#     print("Starting ingestion...")

#     # Load documents
#     documents = load_documents(RAW_DOCS_PATH)
#     print(f"Loaded {len(documents)} documents")

#     # Chunking (IMPORTANT)
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=800,
#         chunk_overlap=100
#     )

#     chunks = []
#     metadatas = []

#     for doc in documents:
#         split_texts = splitter.split_text(doc["content"])

#         for i, chunk in enumerate(split_texts):
#             chunks.append(chunk)
#             metadatas.append(create_metadata(doc, i))

#     print(f"Total chunks: {len(chunks)}")

#     # Embedding
#     embedder = EmbeddingService()
#     embeddings = embedder.embed_texts(chunks)

#     # FAISS
#     dim = len(embeddings[0])
#     vector_store = FAISSStore(dim, FAISS_PATH)
#     vector_store.add_vectors(embeddings)
#     vector_store.save()

#     # Metadata
#     metadata_store = MetadataStore(METADATA_PATH)

#     # chunks Storing
#     with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
#         json.dump(chunks, f, indent=2)

#     for meta in metadatas:
#         metadata_store.add(meta)

#     metadata_store.save()

#     print("Ingestion completed successfully")


# if __name__ == "__main__":
#     run_ingestion()


import os
from app.services.ingestion_service import IngestionService
from app.core.config import settings


def run_bulk_ingestion():

    service = IngestionService()

    files = os.listdir(settings.RAW_DOCS_PATH)

    print(f"📂 Found {len(files)} files")

    total_chunks = 0

    for file in files:
        file_path = os.path.join(settings.RAW_DOCS_PATH, file)

        try:
            result = service.ingest_file(file_path)
            total_chunks += result["chunks_added"]

        except Exception as e:
            print(f"❌ Failed for {file}: {e}")

    print(f"✅ Total chunks added: {total_chunks}")


if __name__ == "__main__":
    run_bulk_ingestion()