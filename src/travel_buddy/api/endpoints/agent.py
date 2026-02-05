"""Agent endpoints."""

from fastapi import APIRouter
from travel_buddy.agents.agent import TravelBuddyAgent
from pydantic import BaseModel
from typing import List, Any
from pydantic_ai.messages import ModelMessagesTypeAdapter

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    country: str
    history: List[Any] | None = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    detected_city: str | None = None
    history: List[Any] = []
    


@router.post("/chat", response_model=ChatResponse)
async def agent_chat( request:ChatRequest):

    travel_agent = TravelBuddyAgent(country=request.country)
    
    valid_history = []
    if request.history:
        cleaned_history = []
        for msg in request.history:
            if isinstance(msg, dict) and "parts" in msg:
                new_parts = []
                for part in msg["parts"]:
                    url = part.get("url") if isinstance(part, dict) else None
                    if url and isinstance(url, str):
                        # Kolla om det är en riktig bild
                        base_url = url.split('?')[0].lower()
                        is_real_image = any(base_url.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])
                        
                        # Om det inte är en bild men tolkas som en media-part:
                        if not is_real_image and (part.get("part_kind") == "image-url" or "url" in part):
                            new_parts.append({"part_kind": "text", "content": f"Länk: {url}"})
                            continue
                    new_parts.append(part)
                msg["parts"] = new_parts
            cleaned_history.append(msg)

        try:
            valid_history = ModelMessagesTypeAdapter.validate_python(cleaned_history)
        except Exception as e:
            print(f"Historik-validering misslyckades: {e}")
            valid_history = []



    result = await travel_agent.ask(request.query, history=valid_history)

    return ChatResponse(
        response=result["ai"],
        sources=result["sources"],
        detected_city=result["detected_city"],
        history=ModelMessagesTypeAdapter.dump_python(result["history"]),
    )