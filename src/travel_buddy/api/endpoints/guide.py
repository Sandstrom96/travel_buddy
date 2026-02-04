"""Guide endpoints."""
from fastapi import APIRouter, HTTPException
from travel_buddy.services.guide_service import GuideService
from travel_buddy.schemas.destination import DestinationGuide, Destination

router = APIRouter()
guide_service = GuideService()


@router.get("/")
async def list_guides() -> dict:
    """List all destinations available as guides."""
    destinations = guide_service.get_all_destinations()
    return {
        "destinations": [
            {"id": d.id, "name": d.name, "country": d.country}
            for d in destinations
        ]
    }


@router.get("/{destination_id}")
async def get_guide(destination_id: str) -> DestinationGuide:
    """Get complete travel guide for a destination.
    
    Args:
        destination_id: Destination ID (e.g., 'tokyo', 'kyoto', 'osaka')
        
    Returns:
        Complete guide with attractions and events
    """
    guide = guide_service.get_guide(destination_id)
    
    if not guide:
        raise HTTPException(
            status_code=404,
            detail=f"Destination '{destination_id}' not found"
        )
    
    return guide