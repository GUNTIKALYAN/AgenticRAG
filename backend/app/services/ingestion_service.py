import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.helpers import load_file
from app.services.embedding_service import EmbeddingService
from app.db.faiss_store import FAISSStore
from app.db.metadata_store import MetadataStore
from app.core.config import settings


class IngestionService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.vector_store = FAISSStore(
            dim=settings.EMBEDDING_DIM,
            index_path=settings.FAISS_INDEX_PATH
        )

        self.metadata_store = MetadataStore(settings.METADATA_PATH)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )


    def ingest_file(self, file_path: str):

        print(f"Ingesting: {file_path}")

        # 1. Load file
        text = load_file(file_path)

        if not text or len(text.strip()) == 0:
            raise Exception("Empty file content")

        # 2. Chunking
        chunks = self.splitter.split_text(text)

        print(f"Chunks created: {len(chunks)}")

        # 3. Embedding
        embeddings = self.embedder.embed_texts(chunks)
        print(f"Embeddings generated: {len(embeddings)}")

        # 4. Prepare metadata 
        metadata_batch = []

        for i, chunk in enumerate(chunks):
            metadata_batch.append({
                "source": os.path.basename(file_path),
                "text": chunk,
                "chunk_id": i
            })
        print(f"Metadata size now: {len(self.metadata_store.data)}")

        # 5. Add to FAISS
        self.vector_store.add(embeddings)

        # 6. Save FAISS
        self.vector_store.save()

        # 7. Add metadata (APPEND ONLY)
        print("Before adding metadata:", len(self.metadata_store.data))
        self.metadata_store.add_batch(metadata_batch)
        print("After adding metadata:", len(self.metadata_store.data))
        self.metadata_store.save()

        from app.db.metadata_store import MetadataStore
        temp_store = MetadataStore(settings.METADATA_PATH)
        print("Reloaded metadata size:", len(temp_store.data))

        # 8. Save chunks.json (for debugging only)
        self._save_chunks(chunks)

        return {
            "chunks_added": len(chunks),
            "total_vectors": self.vector_store.index.ntotal
        }

    def _save_chunks(self, chunks):

        os.makedirs(os.path.dirname(settings.CHUNKS_PATH), exist_ok=True)

        if os.path.exists(settings.CHUNKS_PATH):
            with open(settings.CHUNKS_PATH, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except:
                    existing = []
        else:
            existing = []

        existing.extend(chunks)

        with open(settings.CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)