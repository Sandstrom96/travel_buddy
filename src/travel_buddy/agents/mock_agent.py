"""Mock agent for MVP testing."""
from travel_buddy.agents.base import BaseAgent


class MockAgent(BaseAgent):
    """Mock travel guide agent for MVP."""

    def query(self, message: str) -> str:
        """Process a query with mock responses.
        
        Args:
            message: User message
            
        Returns:
            Mock response
        """
        return f"Mock response to: {message}"
