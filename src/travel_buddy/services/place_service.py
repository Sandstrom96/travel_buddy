from travel_buddy.schemas.recommendation import Place
from travel_buddy.services.transport_service import TransportService


class PlaceService:
    """Service for finding and filtering places (ice cream shops)."""


    # Mock ice cream shops in Osaka (replace with real data later)
    OSAKA_ICE_CREAM_SHOPS = [
        {
            "id": "gelato_1",
            "name": "Gelateriia Bacchetta",
            "address": "1-9-19 Shinsaibashisuji, Chuo-ku, Osaka",
            "latitude": 34.6725,
            "longitude": 135.5018,
            "category": "ice_cream",
            "rating": 4.5,
            "price_level": 2,
            "menu_items": [
                "Pistachio Gelato (¥450)",
                "Matcha Gelato (¥450)",
                "Mango Sorbet (¥420)",
                "Mixed Berry Gelato (¥450)"
            ],
            "description": "Authentic Italian gelato in the heart of Shinsaibashi"
        },
        {
            "id": "softcream_1",
            "name": "Cremia Dotonbori",
            "address": "1-7-21 Dotonbori, Chuo-ku, Osaka",
            "latitude": 34.6686,
            "longitude": 135.5025,
            "category": "ice_cream",
            "rating": 4.3,
            "price_level": 2,
            "menu_items": [
                "Premium Soft Cream (¥500)",
                "Hokkaido Milk Soft Cream (¥550)",
                "Matcha Soft Cream (¥520)",
                "Seasonal Fruit Soft Cream (¥580)"
            ],
            "description": "Premium Japanese soft serve near Glico sign"
        },
        {
            "id": "parlor_1",
            "name": "Parlor Nishiki",
            "address": "3-5-13 Kitahorie, Nishi-ku, Osaka",
            "latitude": 34.6780,
            "longitude": 135.4910,
            "category": "ice_cream",
            "rating": 4.7,
            "price_level": 3,
            "menu_items": [
                "Artisian Ice Cream Sundae (¥780)",
                "Seasonal Fruit Parfait (¥880)",
                "Chocolate Brownie Ice Cream (¥720)",
                "Green Tea Affogato (¥650)"
            ],
            "description": "Upscale ice cream parlor with creative flavors"
        },
        {
            "id": "shop_1",
            "name": "31 Flavors Namba",
            "address": "2-2-3 Nanbanaka, Naniwa-ku, Osaka",
            "latitude": 34.6618,
            "longitude": 135.5012,
            "category": "ice_cream",
            "rating": 4.0,
            "price_level": 2,
            "menu_items": [
                "Single Scoop (¥390)",
                "Double Scoop (¥540)",
                "Triple Scoop (¥690)",
                "Sundae (¥580)"
            ],
            "description": "Baskin_Robbins chain with classic flavors"
        },
        {
            "id": "traditional_1",
            "name": "Kakigori Uji",
            "address": "1-8-16 Tenma, Kita-ku, Osaka",
            "latitude": 34.6970,
            "longitude": 135.5150,
            "category": "ice_cream",
            "rating": 4.6,
            "price_level": 2,
            "menu_items": [
                "Matcha Kakigori (¥650)",
                "Strawberry Kakigori (¥600)",
                "Mango Kakigori (¥700)",
                "Condensed Milk Ice (¥700)",
            ],
            "description": "Traditional Japanese shaved ice shop"
        }
        
    ]

    @staticmethod
    def search_places(
        user_lat: float,
        user_lon: float,
        category: str = "ice_cream",
        max_results: int = 3
    ) -> list[Place]:
        """Search for places near user location"""
        places = []
        

        # Filtering by category and calculate distance
        for shop_data in PlaceService.OSAKA_ICE_CREAM_SHOPS:
            if shop_data["category"] != category:
                continue

            # Calculate distance from user
            distance = TransportService.calculate_distance(
                user_lat, user_lon,
                shop_data["latitude"], shop_data["longitude"]
            )

            place = Place(
                **shop_data,
                distance_km=round(distance, 2)
            )
            places.append(place)

        # Sorting by distance
        places.sort(key=lambda p: p.distance_km)

        # Returning top N results
        return places[:max_results]
    
    @staticmethod
    def get_place_by_id(place_id: str) -> Place | None:
        """Get a specific place by ID."""
        for shop_data in PlaceService.OSAKA_ICE_CREAM_SHOPS:
            if shop_data["id"] == place_id:
                return Place(**shop_data)
        return None