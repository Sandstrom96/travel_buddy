from pydantic import BaseModel, Field
from typing import Optional


class Airport(BaseModel): 
    code: str
    name: str
    latitude: float
    longitude: float
    distance_to_city_center_km: float


class HotelArea(BaseModel):
    code: str
    name: str
    latitude: float
    description: Optional[str] = None


class TransportRouteRequest(BaseModel):
    origin_lat: float = Field(..., ge=-90, le=90)
    origin_lon: float = Field(..., ge=-180, le=180)
    dest_lat: float = Field(..., ge=-90, le=90)
    dest_lon: float = Field(..., ge=-180, le=180)
