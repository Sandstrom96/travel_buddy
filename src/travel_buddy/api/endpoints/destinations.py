"""Destination endpoints."""
from fastapi import APIRouter, HTTPException
from travel_buddy.services.guide_service import GuideService
from travel_buddy.schemas.destination import Destination

router = APIRouter()
guide_service = GuideService()


@router.get("/", response_model=dict)
async def list_destinations() -> dict:
    """List all destinations."""
    destinations = guide_service.get_all_destinations()
    return {
        "destinations": [
            {"id": d.id, "name": d.name, "country": d.country}
            for d in destinations
        ]
        }



@router.get("/{destination_id}", response_model=Destination)
async def get_destination(destination_id: str) -> Destination:
    """Get destination details."""
    destination = guide_service.get_destination(destination_id)

    if not destination:
        raise HTTPException(
            status_code=404,
            detail=f"Destination '{destination_id}' not found"
        )
    return destination
