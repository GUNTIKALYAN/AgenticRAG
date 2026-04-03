# # from fastapi import APIRouter, UploadFile, File
# # import os

# # from app.services.ingestion_service import IngestionService
# # from app.core.config import settings

# # router = APIRouter()


# # @router.post("/ingest")
# # async def ingest_file(file: UploadFile = File(...)):
# #     service = IngestionService()
# #     results = []

# #     try:
# #         os.makedirs(settings.RAW_DOCS_PATH, exist_ok=True)

# #         file_path = os.path.join(settings.RAW_DOCS_PATH, file.filename)

# #         # Save uploaded file
# #         with open(file_path, "wb") as f:
# #             f.write(await file.read())

# #         # Run ingestion
# #         service = IngestionService()
# #         result = service.ingest_file(file_path)

# #         return {
# #             "status": "success",
# #             "file": file.filename,
# #             "chunks_added": result["chunks_added"],
# #             "total_vectors": result["total_vectors"]
# #         }

# #     except Exception as e:
# #         return {"error": str(e)}

# from fastapi import APIRouter, UploadFile, File
# from typing import List
# import os

# from app.services.ingestion_service import IngestionService
# from app.core.config import settings
# from app.services.agent_router import AgentRouter

# router = APIRouter()

# @router.post("/ingest")
# async def ingest(files: List[UploadFile] = File(...)):

#     agent = AgentRouter()

#     uploaded_files = []

#     for file in files:
#         path = save_file_somewhere(file)
#         agent.retriever.vector_store  # just ensure loaded

#         agent.retriever  # optional warmup

#         agent.current_docs = "latest"
#         agent.active_sources.append(file.filename)

#         ingestion_service.ingest_file(path)

#         uploaded_files.append(file.filename)

#     return {"files": uploaded_files}


# # @router.post("/ingest")
# # async def ingest_files(files: List[UploadFile] = File(...)):

# #     service = IngestionService()

# #     results = []

# #     try:
# #         os.makedirs(settings.RAW_DOCS_PATH, exist_ok=True)

# #         for file in files:

# #             file_path = os.path.join(settings.RAW_DOCS_PATH, file.filename)

# #             # Save file
# #             with open(file_path, "wb") as f:
# #                 f.write(await file.read())

# #             # Ingest file
# #             result = service.ingest_file(file_path)

# #             results.append({
# #                 "file": file.filename,
# #                 "chunks_added": result["chunks_added"],
# #                 "total_vectors": result["total_vectors"]
# #             })

# #         return {
# #             "status": "success",
# #             "files_processed": len(results),
# #             "details": results
# #         }

# #     except Exception as e:
# #         return {"error": str(e)}
    

# @router.post("/reset")
# def reset_session():

#     # Delete FAISS
#     if os.path.exists(settings.FAISS_INDEX_PATH):
#         os.remove(settings.FAISS_INDEX_PATH)

#     # Delete metadata
#     if os.path.exists(settings.METADATA_PATH):
#         os.remove(settings.METADATA_PATH)

#     # Delete chunks
#     if os.path.exists(settings.CHUNKS_PATH):
#         os.remove(settings.CHUNKS_PATH)

#     return {"status": "session reset"}


from fastapi import APIRouter, UploadFile, File
from typing import List
import os

from app.services.ingestion_service import IngestionService
from app.core.config import settings

router = APIRouter()

# 🔥 Utility function (clean + reusable)
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
    """
    ⚠️ This resets GLOBAL storage (use carefully)
    """

    if os.path.exists(settings.FAISS_INDEX_PATH):
        os.remove(settings.FAISS_INDEX_PATH)

    if os.path.exists(settings.METADATA_PATH):
        os.remove(settings.METADATA_PATH)

    if os.path.exists(settings.CHUNKS_PATH):
        os.remove(settings.CHUNKS_PATH)

    return {"status": "reset complete"}