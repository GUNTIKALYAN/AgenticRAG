from fastapi import APIRouter, UploadFile, File
from typing import List
import os

from app.services.ingestion_service import IngestionService
from app.core.config import settings

router = APIRouter()

# Utility function 
def save_file(file: UploadFile) -> str:
    os.makedirs(settings.RAW_DOCS_PATH, exist_ok=True)

    file_path = os.path.join(settings.RAW_DOCS_PATH, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


@router.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):

    ingestion_service = IngestionService()
    uploaded_files = []

    for file in files:
        try:
            # 1. Save file
            file_path = save_file(file)

            # 2. Run ingestion
            ingestion_service.ingest_file(file_path)

            uploaded_files.append(file.filename)

        except Exception as e:
            return {"error": f"{file.filename}: {str(e)}"}

    return {
        "status": "success",
        "files": uploaded_files
    }


@router.post("/reset")
def reset_session():

    if os.path.exists(settings.FAISS_INDEX_PATH):
        os.remove(settings.FAISS_INDEX_PATH)

    if os.path.exists(settings.METADATA_PATH):
        os.remove(settings.METADATA_PATH)

    if os.path.exists(settings.CHUNKS_PATH):
        os.remove(settings.CHUNKS_PATH)

    return {"status": "reset complete"}