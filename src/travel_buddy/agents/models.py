from pydantic import BaseModel


class RagResponse(BaseModel):
    result: str
    sources: list[str]
    regions: list[str]
