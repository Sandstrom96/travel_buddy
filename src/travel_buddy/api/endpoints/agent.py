"""Agent endpoints."""
from fastapi import APIRouter
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

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

