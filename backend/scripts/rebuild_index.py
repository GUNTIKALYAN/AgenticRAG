import os
import shutil
from app.core.config import settings
from app.services.ingestion_service import IngestionService


def rebuild():

    print("Rebuilding entire index...")

    # Delete FAISS
    if os.path.exists(settings.FAISS_DIR):
        shutil.rmtree(settings.FAISS_DIR)
        print("Deleted FAISS index")

    # Delete metadata
    if os.path.exists(settings.METADATA_PATH):
        os.remove(settings.METADATA_PATH)
        print("Deleted metadata")

    # Delete chunks
    if os.path.exists(settings.CHUNKS_PATH):
        os.remove(settings.CHUNKS_PATH)
        print("Deleted chunks")

    # Re-ingest all files
    service = IngestionService()

    files = os.listdir(settings.RAW_DOCS_PATH)

    for file in files:
        file_path = os.path.join(settings.RAW_DOCS_PATH, file)
        service.ingest_file(file_path)

    print("Rebuild completed")


if __name__ == "__main__":
    rebuild()