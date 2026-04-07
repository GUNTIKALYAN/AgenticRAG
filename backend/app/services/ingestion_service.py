# import os
# import json

# from langchain_text_splitters import RecursiveCharacterTextSplitter

# from app.utils.helpers import load_file
# from app.services.embedding_service import EmbeddingService
# from app.core.config import settings
# from app.core.startup import state


# class IngestionService:

#     def __init__(self):

#         self.embedder = EmbeddingService()

#         self.vector_store = state.faiss
#         self.metadata_store = state.metadata

#         self.splitter = RecursiveCharacterTextSplitter(
#             chunk_size=600,
#             chunk_overlap=100
#         )


#     def ingest_file(self, file_path: str):

#         print(f"Ingesting: {file_path}")

#         # 1. Load file
#         text = load_file(file_path)

#         if not text or len(text.strip()) < 20:
#             print(f"Skipping (no usable text): {file_path}")
#             return {
#                 "chunks_added": 0,
#                 "total_vectors": self.vector_store.index.ntotal
#             }
        
#         # 2. Chunking
#         chunks = self.splitter.split_text(text)
#         print(f"Chunks created: {len(chunks)}")

#         # 3. Embeddings
#         embeddings = self.embedder.embed_texts(chunks)
#         print(f"Embeddings generated: {len(embeddings)}")

#         # 4. Prepare metadata
#         metadata_batch = []

#         for i, chunk in enumerate(chunks):
#             metadata_batch.append({
#                 "source": os.path.basename(file_path),
#                 "text": chunk,
#                 "chunk_id": i
#             })

#         # 5. Add to FAISS
#         self.vector_store.add(embeddings)

#         # 6. Add metadata (append)
#         print(f"Metadata before: {len(self.metadata_store.data)}")

#         self.metadata_store.add_batch(metadata_batch)
#         self.metadata_store.save()

#         print(f"Metadata after: {len(self.metadata_store.data)}")

#         # Refresh global state
#         from app.db.metadata_store import MetadataStore
#         from app.services.hybrid_search_service import HybridSearchService

#         state.metadata = MetadataStore(settings.METADATA_PATH)
#         state.hybrid = HybridSearchService(state.metadata)

#         print(f"Global metadata updated: {len(state.metadata.data)}")

#         # 7. Save chunks 
#         self._save_chunks(chunks)

#         return {
#             "chunks_added": len(chunks),
#             "total_vectors": self.vector_store.index.ntotal
#         }

#     def _save_chunks(self, chunks):

#         os.makedirs(os.path.dirname(settings.CHUNKS_PATH), exist_ok=True)

#         if os.path.exists(settings.CHUNKS_PATH):
#             try:
#                 with open(settings.CHUNKS_PATH, "r", encoding="utf-8") as f:
#                     existing = json.load(f)
#             except:
#                 existing = []
#         else:
#             existing = []

#         existing.extend(chunks)

#         with open(settings.CHUNKS_PATH, "w", encoding="utf-8") as f:
#             json.dump(existing, f, indent=2)

import os
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.helpers import load_file
from app.services.embedding_service import EmbeddingService
from app.core.config import settings
from app.core.startup import state


class IngestionService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.vector_store = state.faiss
        self.metadata_store = state.metadata

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )

    def ingest_file(self, file_path: str):

        print(f"📄 Ingesting: {file_path}")

        # 1. Load file
        text = load_file(file_path)

        if not text:
            print(f"❌ Skipped (no usable text): {file_path}")
            return {
                "status": "failed",
                "reason": "No extractable text"
            }

        # 2. Chunking
        chunks = self.splitter.split_text(text)

        if not chunks:
            print(f"❌ No chunks created: {file_path}")
            return {
                "status": "failed",
                "reason": "Chunking failed"
            }

        print(f"✂️ Chunks created: {len(chunks)}")

        # 3. Embeddings
        embeddings = self.embedder.embed_texts(chunks)
        print(f"🧠 Embeddings generated: {len(embeddings)}")

        # 4. Metadata
        metadata_batch = [
            {
                "source": os.path.basename(file_path),
                "text": chunk,
                "chunk_id": i
            }
            for i, chunk in enumerate(chunks)
        ]

        # 5. Store vectors
        self.vector_store.add(embeddings)

        # 6. Store metadata
        print(f"📦 Metadata before: {len(self.metadata_store.data)}")

        self.metadata_store.add_batch(metadata_batch)
        self.metadata_store.save()

        print(f"📦 Metadata after: {len(self.metadata_store.data)}")

        # 7. Refresh global state (important)
        from app.db.metadata_store import MetadataStore
        from app.services.hybrid_search_service import HybridSearchService

        state.metadata = MetadataStore(settings.METADATA_PATH)
        state.hybrid = HybridSearchService(state.metadata)

        print(f"🔄 Global metadata updated: {len(state.metadata.data)}")

        # 8. Save chunks (optional)
        self._save_chunks(chunks)

        return {
            "status": "success",
            "chunks_added": len(chunks),
            "total_vectors": self.vector_store.index.ntotal
        }

    def _save_chunks(self, chunks):

        os.makedirs(os.path.dirname(settings.CHUNKS_PATH), exist_ok=True)

        if os.path.exists(settings.CHUNKS_PATH):
            try:
                with open(settings.CHUNKS_PATH, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except:
                existing = []
        else:
            existing = []

        existing.extend(chunks)

        with open(settings.CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)