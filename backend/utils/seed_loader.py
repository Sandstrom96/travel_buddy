"""Seed data loader for mock data from JSON files."""
import json
from pathlib import Path
from typing import Any

# Path to seed data directory
SEEDS_DIR = Path(__file__).parent.parent.parent.parent / "data" / "seeds"


def load_seed_file(filename: str) -> dict[str, Any]:
    """Load a JSON seed file.
    
    Args:
        filename: Name of the seed file (e.g., 'japan_destinations.json')
        
    Returns:
        Parsed JSON data as dictionary
    """
    file_path = SEEDS_DIR / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_destinations() -> list[dict]:
    """Get all destinations from seed data."""
    data = load_seed_file("japan_destinations.json")
    return data.get("destinations", [])


def get_destination(destination_id: str) -> dict | None:
    """Get specific destination by ID."""
    destinations = get_destinations()
    for dest in destinations:
        if dest["id"] == destination_id:
            return dest
    return None


def get_attractions(destination_id: str | None = None) -> list[dict]:
    """Get attractions, optionally filtered by destination."""
    data = load_seed_file("japan_attractions.json")
    attractions = data.get("attractions", [])
    
    if destination_id:
        attractions = [a for a in attractions if a.get("destination") == destination_id]
    
    return attractions


def get_events(destination_id: str | None = None) -> list[dict]:
    """Get events, optionally filtered by destination."""
    data = load_seed_file("japan_events.json")
    events = data.get("events", [])
    
    if destination_id:
        # Events can have multiple destinations
        events = [e for e in events if destination_id in e.get("destination", [])]
    
    return events


def get_travel_styles() -> dict:
    """Get all travel style categories."""
    data = load_seed_file("japan_travel_styles.json")
    return data.get("travel_styles", {})