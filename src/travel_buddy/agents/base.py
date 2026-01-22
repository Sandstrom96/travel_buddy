"""Base agent class."""
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Abstract base class for agents."""

    @abstractmethod
    def query(self, message: str) -> str:
        """Process a query.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        pass
