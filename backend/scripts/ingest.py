import os
from app.services.ingestion_service import IngestionService
from app.core.config import settings


def run_bulk_ingestion():

    service = IngestionService()

    files = os.listdir(settings.RAW_DOCS_PATH)

    print(f"Found {len(files)} files")

    total_chunks = 0

    for file in files:
        file_path = os.path.join(settings.RAW_DOCS_PATH, file)

        try:
            result = service.ingest_file(file_path)
            total_chunks += result["chunks_added"]

        except Exception as e:
            print(f" Failed for {file}: {e}")

    print(f"Total chunks added: {total_chunks}")


if __name__ == "__main__":
    run_bulk_ingestion()