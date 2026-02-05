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
        
    
    @staticmethod
    def get_airport_transport(distance_km: float) -> list:
        from travel_buddy.schemas.recommendation import TransportOption

        options = []

        train_fare = TransportService.get_train_fare(distance_km)
        train_time = int(distance_km * 1.5)
        options.append(TransportOption(
            mode="train",
            route_name="JR Express / Airport Train",
            duration_minutes = train_time,
            price_jpy=train_fare,
            distance_km=distance_km,
            instructions=f"Take JR or airport express train. Approx {train_time} minutes."
        ))

        bus_fare = 1500 if distance_km < 30 else 2000
        bus_time = int(distance_km * 2)
        options.append(TransportOption(
            mode="bus",
            route_name="Airports Limousine Bus",
            duration_minutes=bus_fare,
            price_jpy=bus_fare,
            distance_km=distance_km,
            instructions=f"Direct airport bus service. Approx {bus_time} minutes."
        ))

        
        taxi_fare= TransportService.TAXI_BASE_FARE + int(distance_km * TransportService.TAXI_PER_KM * 4)
        taxi_time = int(distance_km * 1.2)
        options.append(TransportOption(
            mode="taxi",
            route_name="Taxi",
            duration_minutes=taxi_time,
            price_jpy=taxi_fare,
            distance_km=distance_km,
            instructions=f"Private taxi. Approx {taxi_time} minutes. Expensive for long distances."
        ))

        return options

    @staticmethod
    def get_train_fare(distance_km: float) -> int:
        if distance_km < 20:
            return 500
        elif distance_km < 40:
            return 1000
        elif distance_km < 60:
            return 1500
        elif distance_km < 80:
            return 2500
        else: 
            return 3500