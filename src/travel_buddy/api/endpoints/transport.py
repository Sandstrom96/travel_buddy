"""Transport endpoints for airports and routes."""
from fastapi import APIRouter, HTTPException, Path
from travel_buddy.schemas.transport import Airport, HotelArea, TransportRouteRequest
from travel_buddy.schemas.recommendation import TransportOption
from travel_buddy.data.airports import AIRPORTS, HOTEL_AREAS
from travel_buddy.services.transport_service import TransportService

router = APIRouter()


@router.get("/airports/{city}", response_model=list[Airport])
async def get_airports(city: str = Path(..., pattern="^(osaka|tokyo|kyoto)$")):
    city_lower = city.lower()

    if city_lower not in AIRPORTS:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    airports = [Airport(**airport) for airport in AIRPORTS[city_lower]]
    return airports

@router.get("/hotels/{city}", response_model=list[HotelArea])
async def get_hotel_areas(city: str = Path(..., pattern="^(osaka|tokyo|kyoto)$")):
    city_lower = city.lower()

    if city_lower not in HOTEL_AREAS:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    hotel_areas = [HotelArea(**area) for area in HOTEL_AREAS[city_lower]]
    return hotel_areas


@router.post("/route", response_model=list[TransportOption])
async def get_transport_route(request: TransportRouteRequest):
    distance = TransportService.calculate_distance(
        request.origin_lat,
        request.origin_lon,
        request.dest_lat,
        request.dest_lon
    )

    if distance > 10:
        options = TransportService.get_airport_transport(distance)
    else:
        options = TransportService.get_transport_options(
            request.origin_lat,
            request.origin_lon,
            request.dest_lat,
            request.dest_lon
        )

    return options