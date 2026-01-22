"""Agent schemas."""
from pydantic import BaseModel


class Message(BaseModel):
    """Message schema for agent communication."""
    content: str
    role: str = "user"


class AgentResponse(BaseModel):
    """Agent response schema."""
    response: str
    context: str | None = None
