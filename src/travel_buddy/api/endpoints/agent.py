"""Agent endpoints."""

from fastapi import APIRouter
from travel_buddy.agents.agent import TravelBuddyAgent
from pydantic import BaseModel
from typing import Optional, List, Any

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    country: str
    history: Optional[List[Any]] = []


@router.post("/chat")
async def agent_chat(request: ChatRequest):
    agent = TravelBuddyAgent(country=request.country)
    result = await agent.ask(user_query=request.message, history=request.history)
    return result
