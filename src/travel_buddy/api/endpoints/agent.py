"""Agent endpoints."""

from fastapi import APIRouter
from travel_buddy.agents.agent import TravelBuddyAgent
from pydantic import BaseModel
from typing import Optional, List, Any

router = APIRouter()
chat_histories: Dict[str, List[ModelMessage]] = {}

agent = Agent(
    "google-gla:gemini-2.0-flash",
    system_prompt="Du är Travel Buddy, en expert på resor till Japan. Hjälp användaren med detaljerad information om sevärdheter, kultur och resplaner",
)

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

    result = await agent.run(user_query, message_history=message_history)

    if thread_id:
        chat_histories[thread_id] = result.all_messages()
    return ChatResponse(response=result.output)

class ChatRequest(BaseModel):
    message: str
    country: str
    history: Optional[List[Any]] = []


@router.post("/chat")
async def agent_chat(request: ChatRequest):
    agent = TravelBuddyAgent(country=request.country)
    result = await agent.ask(user_query=request.message, history=request.history)
    return result
