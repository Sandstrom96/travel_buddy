"""Destination endpoints."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_destinations():
    """List all destinations."""
    return {"destinations": []}


@router.get("/{destination_id}")
async def get_destination(destination_id: str):
    """Get destination details."""
    return {"destination_id": destination_id}
