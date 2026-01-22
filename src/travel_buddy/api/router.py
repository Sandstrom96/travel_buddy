"""Main router collecting all endpoint routers."""
from fastapi import APIRouter

from travel_buddy.api.endpoints import health, destinations, guide, agent

router = APIRouter()

# Include all endpoint routers
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(destinations.router, prefix="/destinations", tags=["destinations"])
router.include_router(guide.router, prefix="/guide", tags=["guide"])
router.include_router(agent.router, prefix="/agent", tags=["agent"])
