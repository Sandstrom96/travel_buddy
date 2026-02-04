from travel_buddy.schemas.recommendation import  ActivityRecommendation
from travel_buddy.services.place_service import PlaceService
from travel_buddy.services.transport_service import TransportService
from travel_buddy.services.weather_service import WeatherService


class RecommendationService:
    """Orchestrate recommendations with places, transport, and weather."""

    @staticmethod
    async def get_activity_recommendations(
        user_lat: float,
        user_lon: float,
        activity_type: str = "ice_cream",
        max_results: int = 3
    ) -> list[ActivityRecommendation]:
        """Get complete activity recommendations"""

        places = PlaceService.search_places(
            user_lat=user_lat,
            user_lon=user_lon,
            category=activity_type,
            max_results=max_results
        )

        if places:
            weather = await WeatherService.get_weather(places[0].latitude, places[0].longitude)
        else:
            # Fallback to Osaka center
            weather = await WeatherService.get_weather(34.6937, 135.5023)

        recommendations = []
        for place in places:
            # Transport options
            transport_options = TransportService.get_transport_options(
                from_lat=user_lat,
                from_lon=user_lon,
                to_lat=place.latitude,
                to_lon=place.longitude
            )

            # Calculating recommendation score
            score = RecommendationService._calculate_score(
                place=place,
                weather=weather,
                distance_km=place.distance_km
            )

            reason = RecommendationService._generate_reason(
                place=place,
                weather=weather,
                cheapest_transport=transport_options[0] if transport_options else None
            )

            recommendation = ActivityRecommendation(
                place=place,
                transport_options=transport_options,
                weather=weather,
                recommendation_score=score,
                reason=reason
            )
            recommendations.append(recommendation)

        recommendations.sort(key=lambda r: r.recommendation_score, reverse=True)
        
        return recommendations

    @staticmethod
    def _calculate_score(place, weather, distance_km: float) -> float:
        """Calculate recommendation score (0-1)."""
        score = 0.5 

        if distance_km < 1:
            score += 0.2
        elif distance_km < 2:
            score += 0.1

        if place.rating:
            score += (place.rating - 3) * 0.1

        if weather.temperature_celsius > 25:
            score += 0.1
        elif weather.temperature_celsius < 15:
            score -= 0.1

        if weather.precipitation_chance > 50:
            score -= 0.1

        return max(0.0, min(1.0, score))
    
    @staticmethod
    def _generate_reason(place, weather, cheapest_transport) -> str:
        """Generate reasonable recommendations"""
        reasons = []

        if place.distance_km < 2:
            reasons.append("Very close by")
        elif place.distance_km < 2:
            reasons.append("Short distance")

        if place.rating and place.rating >= 4.5:
            reasons.append(f"highly rated ({place.rating}★)")

        if weather.temperature_celsius > 25:
            reasons.append("perfect ice cream weather")

        if cheapest_transport and cheapest_transport.price_jpy == 0:
            reasons.append("walking distance")
        elif cheapest_transport:
            reasons.append(f"¥{cheapest_transport.price_jpy} by {cheapest_transport.mode}")

        return ", ".join(reasons) if reasons else "Good option in your area"



