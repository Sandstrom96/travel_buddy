from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from travel_buddy.schemas.recommendation import ActivityRecommendation
from travel_buddy.services.recommendation_service import RecommendationService


router = APIRouter()


class RecommendationRequest(BaseModel):
    user_latitude: float = Field(..., ge=-90, le=90)
    user_longitude: float = Field(..., ge=-180, le=180)
    activity_type: str = Field(default="temple") 
    max_results: int = Field(default=5, ge=1, le=10)

@router.post("/", response_model=list[ActivityRecommendation])
async def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = await RecommendationService.get_activity_recommendations(
            user_lat=request.user_latitude,
            user_lon=request.user_longitude,
            activity_type=request.activity_type,
            max_results=request.max_results,
        )

        if not recommendations:
            return []

        return recommendations

    except Exception as e:
        print(f"DEBUG: Recommendation Error: {e}")
        raise HTTPException(status_code=500, detail="Ett oväntat fel uppstod vid hämtning av rekommendationer.")


@router.get("/example")
async def get_example_recommendations():
    """
    Get example recommendation for Dotonbori area in Osaka.
    Useful for testing without providing coordinates.
    """

    # Dotonbori coordinates (near Glico sign)
    recommendations = await RecommendationService.get_activity_recommendations(
        user_lat=34.6686, user_lon=135.5023, activity_type="ice_cream", max_results=3
    )
    return recommendations
