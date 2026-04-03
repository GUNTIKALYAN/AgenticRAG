# import os
# import shutil
# import subprocess

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# DATA_DIR = os.path.join(BASE_DIR, "data")
# FAISS_DIR = os.path.join(DATA_DIR, "faiss")
# METADATA_PATH = os.path.join(DATA_DIR, "metadata", "metadata.json")


# def rebuild():

#     print("⚠️ Rebuilding entire index...")

#     # Delete FAISS index
#     if os.path.exists(FAISS_DIR):
#         shutil.rmtree(FAISS_DIR)
#         print("🗑️ Deleted FAISS index")

#     # Reset metadata
#     if os.path.exists(METADATA_PATH):
#         os.remove(METADATA_PATH)
#         print("🗑️ Deleted metadata")

#     # Re-run ingestion
#     subprocess.run(["python", "backend/scripts/ingest.py"], check=True)

#     print("✅ Rebuild completed")


# if __name__ == "__main__":
#     rebuild()

import os
import shutil
from app.core.config import settings
from app.services.ingestion_service import IngestionService


def rebuild():

    print("⚠️ Rebuilding entire index...")

    # Delete FAISS
    if os.path.exists(settings.FAISS_DIR):
        shutil.rmtree(settings.FAISS_DIR)
        print("🗑️ Deleted FAISS index")

    # Delete metadata
    if os.path.exists(settings.METADATA_PATH):
        os.remove(settings.METADATA_PATH)
        print("🗑️ Deleted metadata")

    # Delete chunks
    if os.path.exists(settings.CHUNKS_PATH):
        os.remove(settings.CHUNKS_PATH)
        print("🗑️ Deleted chunks")

    # Re-ingest all files
    service = IngestionService()

    files = os.listdir(settings.RAW_DOCS_PATH)

    for file in files:
        file_path = os.path.join(settings.RAW_DOCS_PATH, file)
        service.ingest_file(file_path)

    print("✅ Rebuild completed")


if __name__ == "__main__":
    rebuild()