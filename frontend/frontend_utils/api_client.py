"""API client for backend communication."""
import httpx
import os


class APIClient:
    """Client for communicating with Travel Buddy API."""

    def __init__(self, base_url: str | None = None):
        """Initialize API client.
        
        Args:
            base_url: Backend API base URL
        """
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:8000")

    async def get_guide(self, destination: str) -> dict:
        """Get travel guide for destination.
        
        Args:
            destination: Destination name
            
        Returns:
            Guide data
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/guide/{destination}")
            return response.json()

    async def query_agent(self, message: str) -> str:
        """Query travel agent.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/agent/chat",
                params={"message": message}
            )
            return response.json()
