"""Agent endpoints."""

from fastapi import APIRouter
from travel_buddy.agents.agent import TravelBuddyAgent
from pydantic import BaseModel
from typing import List
from pydantic_ai.messages import ModelMessage
from travel_buddy.agents.agent import TravelBuddyAgent
from typing import Dict

router = APIRouter()
travel_agent = TravelBuddyAgent()
chat_histories: Dict[str, List[ModelMessage]] = {}

class ChatRequest(BaseModel):
    query: str
    thread_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    


@router.post("/chat", response_model=ChatResponse)
async def agent_chat( request:ChatRequest):
    user_query = request.query
    thread_id = request.thread_id
    message_history = chat_histories.get(thread_id) if thread_id else None
    result = await travel_agent.ask(user_query, history=message_history)

    if thread_id:
        chat_histories[thread_id] = result.all_messages()
    return ChatResponse(response=result.output)