from app.core.startup import state
from app.db.faiss_store import FAISSStore
from app.db.metadata_store import MetadataStore
from app.services.hybrid_search_service import HybridSearchService
from app.core.config import settings
import os
def reset_session():

    # delete files
    for path in [
        settings.FAISS_INDEX_PATH,
        settings.METADATA_PATH,
        settings.CHUNKS_PATH
    ]:
        if os.path.exists(path):
            os.remove(path)

    # reset memory state
    state.faiss = FAISSStore(dim=settings.EMBEDDING_DIM)
    state.metadata = MetadataStore(settings.METADATA_PATH)
    state.hybrid = HybridSearchService(state.metadata)

    print("🧹 Full session reset")

    return True