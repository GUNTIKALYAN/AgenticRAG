from fastapi import APIRouter
from app.services.session_service import reset_session

router = APIRouter()


@router.post("/new-chat")
def new_chat():
    reset_session()
    return {"status": "session reset"}