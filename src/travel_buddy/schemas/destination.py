"""Destination schemas."""
from pydantic import BaseModel


class DestinationBase(BaseModel):
    """Base destination schema."""
    name: str
    country: str
    description: str | None = None


class DestinationCreate(DestinationBase):
    """Schema for creating a destination."""
    pass


class Destination(DestinationBase):
    """Destination response schema."""
    id: int

    class Config:
        from_attributes = True
