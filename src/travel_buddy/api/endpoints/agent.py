from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from travel_buddy.services.rag_service import RAGService
from typing import Optional

router = APIRouter(prefix="/agent", tags=["agent"])

rag_service = None

def get_rag_service():
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service


class ChatRequest(BaseModel):
    message: str
    destination: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sources: list[dict]
    context_used: int


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print(f"DEBUG ENDPOINT: Received request: {request.message}")
    try:
        print("DEBUG ENDPOINT: Getting RAG service...")
        service = get_rag_service()
        print("DEBUG ENDPOINT: Calling query...")
        result = service.query(
            question=request.message,
            destination=request.destination
        )
        print(f"DEBUG ENDPOINT: Got result with answer length: {len(result['answer'])}")

        return ChatResponse(
            response=result["answer"],
            sources=result["sources"],
            context_used=result["context_used"]
        )
    except Exception as e:
        print(f"ERROR ENDPOINT: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/")
async def agent_info():
    return {
        "name": "Travel Buddy AI",
        "description": "AI travel guide powered by RAG",
        "example_questions": [
            "What are the visa requirements for Japan?",
            "Tell me more about Fushimi Inari shrine",
            "When is the best time to see cherry blossoms?",
            "What can I do in Tokyo?",
            "Tell me more about Gion Matsuri festival"
        ]
    }

