import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings:

    APP_NAME = "Agentic RAG"

    DATA_DIR = os.path.join(BASE_DIR, "data")

    RAW_DOCS_PATH = os.path.join(DATA_DIR, "raw_docs")
    PROCESSED_PATH = os.path.join(DATA_DIR, "processed")
    CHUNKS_PATH = os.path.join(PROCESSED_PATH, "chunks.json")

    FAISS_DIR = os.path.join(DATA_DIR, "faiss")
    FAISS_INDEX_PATH = os.path.join(FAISS_DIR, "index.bin")

    METADATA_DIR = os.path.join(DATA_DIR, "metadata")
    METADATA_PATH = os.path.join(METADATA_DIR, "metadata.json")

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    LLM_API_KEY = os.getenv("GROQ_API_KEY", "")


settings = Settings()