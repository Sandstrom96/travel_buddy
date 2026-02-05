from fastapi import APIRouter
from travel_buddy.api.endpoints import (
    health,
    destinations,
    guide,
    agent,
    recommendations,
    weather,
    transport,
)

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(
    destinations.router, prefix="/destinations", tags=["destinations"]
)
router.include_router(guide.router, prefix="/guide", tags=["guide"])
router.include_router(agent.router, prefix="/agent", tags=["agent"])
router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)
router.include_router(weather.router, prefix="/weather", tags=["weather"])
router.include_router(transport.router, prefix="/transport", tags=["transport"])
