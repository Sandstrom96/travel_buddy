from pydantic import BaseModel, Field
from typing import Optional


class Place(BaseModel):
    """Ice cream shop or restaurant details."""

    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    category: str = "ice_cream"
    rating: Optional[float] = None
    price_level: Optional[int] = Field(None, ge=1, le=4)
    distance_km: Optional[float] = None
    menu_items: list[str] = []
    description: Optional[str] = None


class TransportOption(BaseModel):
    """Transportation option with pricing."""

    mode: str  # metro, taxi, bus, walk
    route_name: Optional[str] = None  # e.g., Midosuji Line
    duration_minutes: int
    price_jpy: int  # Japan Yen
    instructions: Optional[str] = None
    distance_km: Optional[float] = None


class WeatherInfo(BaseModel):
    """Current weather information."""

    temperature_celsius: float
    conditions: str  # Clear, Cloudy, Rainy
    precipitation_chance: int  # 0-100%
    humidity: int  # 0-100%
    wind_speed_kmh: float
    feels_like_celsius: float
    needs_umbrella: bool = False
    daily_max_temperature: float
    daily_min_temperature: float
    uv_index: float
    needs_sunscreen: bool = False


class ActivityRecommendation(BaseModel):
    """Complete recommendation with place, transportation, and weather."""

    place: Place
    transport_options: list[TransportOption]
    weather: WeatherInfo
    recommendation_score: float = Field(ge=0, le=1)  # 0-1
    reason: Optional[str] = None  # Why recommended
