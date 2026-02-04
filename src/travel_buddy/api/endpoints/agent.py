"""Agent endpoints."""

from fastapi import APIRouter
from travel_buddy.agents.agent import TravelBuddyAgent
from pydantic import BaseModel
from typing import List, Dict
from pydantic_ai.messages import ModelMessage


router = APIRouter()

chat_histories: Dict[str, List[ModelMessage]] = {}

class ChatRequest(BaseModel):
    query: str
    country: str
    thread_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    detected_city: str | None = None
    


@router.post("/chat", response_model=ChatResponse)
async def agent_chat( request:ChatRequest):
    user_query = request.query
    thread_id = request.thread_id
    travel_agent = TravelBuddyAgent(country=request.country)
    message_history = chat_histories.get(thread_id) if thread_id else None
    result = await travel_agent.ask(user_query, history=message_history)

    if thread_id:
        chat_histories[thread_id] = result["history"]

    return ChatResponse(
        response=result["ai"],
        sources=result["sources"],
        detected_city=result("detected_city"),
    )