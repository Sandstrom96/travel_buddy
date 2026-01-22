"""Guide schemas."""
from pydantic import BaseModel


class GuideSection(BaseModel):
    """Guide section schema."""
    title: str
    content: str


class TravelGuide(BaseModel):
    """Travel guide schema."""
    destination: str
    sections: list[GuideSection]
