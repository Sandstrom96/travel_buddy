""" Guide service - handles guide generation and retrieval."""
from utils.seed_loader import (
    get_destination,
    get_attractions,
    get_events,
    get_destinations as get_all_destinations_data,
)
from backend.schemas.destination import (
Destination,
Attraction,
Event,
DestinationGuide,
)

class GuideService:
    """Service for managing travel guides."""
    @staticmethod
    def get_all_destinations() -> list[Destination]:
        """Get all destinations."""
        dests = get_all_destinations_data()
        return [Destination(**d) for d in dests]
    
    @staticmethod 
    def get_destination(destination_id: str) -> Destination | None:
        """Get a single destination by ID."""
        dest_data = get_destination(destination_id)
        if not dest_data:
            return None
        return Destination(**dest_data)
    
    @staticmethod
    def get_guide(destination_id: str) -> DestinationGuide | None:
        """Get complete travel guide for a destination"""
        dest_data = get_destination(destination_id)
        if not dest_data:
            return None
        
        destination = Destination(**dest_data)
        attractions = [Attraction(**a) for a in get_attractions(destination_id)]
        events = [Event(**e) for e in get_events(destination_id)]

        return DestinationGuide(
            destination=destination,
            attractions=attractions,
            events=events,
        )