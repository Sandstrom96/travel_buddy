from travel_buddy.services.weather_service import WeatherService
from travel_buddy.schemas.recommendation import WeatherInfo
from fastapi import APIRouter

router = APIRouter()


@router.get("/{city}", response_model=WeatherInfo)
async def get_weather(city: str):
    """Get wheather information for a given city."""
    location = await WeatherService.get_location_coordinates(city=city)
    weather = await WeatherService.get_weather(
        latitude=location["lat"], longitude=location["lon"]
    )
    return weather
