"""Agent endpoints."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    thread_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    


@router.post("/chat", response_model=ChatResponse)
async def agent_chat( request:ChatRequest):
    user_query = request.query

    fake_ai_response = f"Jag hörde att du sa: '{user_query}'. Jag är redo att kopplas till AI-hjärnan!"
    return ChatResponse(response=fake_ai_response)

