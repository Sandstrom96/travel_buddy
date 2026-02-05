import requests
import os
from typing import Optional
import httpx

class APIClient:
    """Client for Travel Buddy API."""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:8000")

    
    def get_destinations(self) -> dict:
        """Get all destinations."""
        response = httpx.get(f"{self.base_url}/destinations/")
        response.raise_for_status()
        return response.json()
    
    
    def get_destination(self, destination_id: str) -> dict:
        """Get single destination."""
        response = httpx.get(f"{self.base_url}/destinations/{destination_id}")
        response.raise_for_status()
        return response.json()
    
    
    def get_guide(self, destination_id: str) -> dict:
        """Get destination guide."""
        response = httpx.get(f"{self.base_url}/guide/{destination_id}")
        response.raise_for_status()
        return response.json()
    
    
    def get_recommendations(
            self,
            user_lat: float,
            user_lon: float,
            activity_type: str = "ice_cream",
            max_results: int = 3
    ) -> list[dict]:
        """Get activity recommendations."""
        response = httpx.post(
            f"{self.base_url}/recommendations/",
            json={
                "user_latitude": user_lat,
                "user_longitude": user_lon,
                "activity_type": activity_type,
                "max_results": max_results
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    
    def get_example_recommendations(self) -> list[dict]:
        """Get example recommendations"""
        response = httpx.get(f"{self.base_url}/recommendations/example")
        response.raise_for_status()
        return response.json()
    

    def chat_with_agent(
            self,
            message: str,
            destination: Optional[str] = None
    ) -> dict:
        response = httpx.post(
            f"{self.base_url}/agent/agent/chat",
            json={
                "message": message,
                "destination": destination
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    
    
    def get_example_questions(self) -> dict:
        response = httpx.get(f"{self.base_url}/agent/agent")
        response.raise_for_status()
        return response.json()