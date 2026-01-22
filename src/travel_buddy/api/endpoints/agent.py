"""Agent endpoints."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def agent_chat(message: str):
    """Chat with travel guide agent."""
    return {"message": message, "response": ""}
