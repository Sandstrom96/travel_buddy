import httpx
from travel_buddy.schemas.recommendation import WeatherInfo


class WeatherService:
    """Free weather service using Open_Meteo API"""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    async def get_weather(latitude: float, longitude: float) -> WeatherInfo:
        """Get current weather coordinates."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
            "timezone": "Asia/Tokyo"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherService.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        current = data["current"]

        
        weather_code = current.get("weather_code", 0)
        conditions = WeatherService._map_weather_code(weather_code)

        return WeatherInfo(
            temperature_celsius=current["temperature_2m"],
            conditions=conditions,
            precipitation_chance=int(current.get("precipitation", 0) * 10),
            humidity=current["relative_humidity_2m"],
            wind_speed_kmh=current["wind_speed_10m"],
            feels_like_celsius=current["temperature_2m"] - (current["wind_speed_10m"] * 0.2)
        )
    
    @staticmethod
    def _map_weather_code(code: int) -> str:
        """Mapping WMO weather codes to simple conditions"""
        if code == 0:
            return "Clear"
        elif code in [1,2, 3]:
            return "Partly Cloudy"
        elif code in [45,48]:
            return "Foggy"
        elif code in [51, 53, 55, 56, 57]:
            return "Drizzle"
        elif code in [61, 63, 65, 66, 67]:
            return "Rainy"
        elif code in [71, 73, 75, 77]:
            return "Snowy"
        elif code in [80, 81, 82]:
            return "Rain Showers"
        elif code in [85, 86]:
            return "Snow Showers"
        elif code in [95, 96, 99]:
            return "Thunderstorm"
        else: 
            return "Cloudy"