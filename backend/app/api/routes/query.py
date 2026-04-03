from fastapi import APIRouter
from app.services.agent_router import AgentRouter
from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest):
    
    agent = AgentRouter()

    return agent.handle_query(payload.query)