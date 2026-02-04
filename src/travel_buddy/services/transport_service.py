import math
from travel_buddy.schemas.recommendation import TransportOption


class TransportService:
    """ Calculate transport options and pricing for Osaka"""

    # Osaka Metro base fare structure
    SUBWAY_BASE_FARE = 180 # ¥180 for 0-3km
    SUBWAY_MID_FARE = 230 # ¥230 for 3-7km
    SUBWAY_LONG_FARE = 280 # ¥280 for 7-11km
    SUBWAY_MAX_FARE = 380 # ¥380 for 11km+

    # Taxi pricing
    TAXI_BASE_FARE = 660 # ¥660 for first 1.7km
    TAXI_PER_KM = 80 # ¥80 per 250m after base

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance in km using Haversine formula."""
        R = 6371 # Earth radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c
    
    @staticmethod 
    def get_transport_options(
        from_lat: float,
        from_lon: float,
        to_lat: float,
        to_lon: float,
    ) -> list[TransportOption]:
        """Get transport options with pricing."""
        distance_km = TransportService.calculate_distance(from_lat, from_lon, to_lat, to_lon)

        options = []
        

        # Walking option (if < 2km)
        if distance_km < 2.0:
            walk_duration = int(distance_km * 12)
            options.append(TransportOption(
                mode="walk",
                duration_minutes=walk_duration,
                price_jpy=0,
                distance_km=round(distance_km, 2),
                instructions=f"Walk {distance_km:.1f}km"
            ))

        
        # Subway Option
        subway_price = TransportService._calculate_subway_fare(distance_km)
        subway_duration = int(distance_km * 4 + 10) # ~4 min per km + 10 min wait/transfer
        options.append(TransportOption(
            mode="subway",
            route_name="Osaka Metro",
            duration_minutes=subway_duration,
            price_jpy=subway_price,
            distance_km=round(distance_km, 2),
            instructions="Take Osaka Metro (route varies by location)"
        ))


        # Taxi option
        taxi_price = TransportService._calculate_taxi_fare(distance_km)
        taxi_duration = int(distance_km * 5) # ~5 min per km in traffic
        options.append(TransportOption(
            mode="taxi",
            duration_minutes=taxi_duration,
            price_jpy=taxi_price,
            distance_km=round(distance_km, 2),
            instructions=f"Taxi from current location (~¥{taxi_price})"
        ))

        
        # Sort by price (cheapest first)
        options.sort(key=lambda x: x.price_jpy)

        return options
    
    @staticmethod
    def _calculate_subway_fare(distance_km: float) -> int:
        """Calculate Osaka Metro fare based on distance"""
        if distance_km <= 3:
            return TransportService.SUBWAY_BASE_FARE
        elif distance_km <= 7:
            return TransportService.SUBWAY_MID_FARE
        elif distance_km <= 11:
            return TransportService.SUBWAY_LONG_FARE
        else:
            return TransportService.SUBWAY_MAX_FARE
        
        
    @staticmethod
    def _calculate_taxi_fare(distance_km: float) -> int:
        """Calculate taxi fare for Osaka"""
        if distance_km <= 1.7:
            return TransportService.TAXI_BASE_FARE
        else:
            extra_km = distance_km - 1.7
            extra_fare = int(extra_km * 4) * TransportService.TAXI_PER_KM # Per 250m
            return TransportService.TAXI_BASE_FARE + extra_fare