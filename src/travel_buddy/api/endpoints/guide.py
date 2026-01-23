"""Guide endpoints."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/{destination}")
async def get_guide(destination: str):
    """Get travel guide for a destination."""
    return {"destination": destination, "guide": {}}
