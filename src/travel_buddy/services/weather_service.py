import httpx
from travel_buddy.schemas.recommendation import WeatherInfo


class WeatherService:
    """Free weather service using Open_Meteo API"""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"

    @staticmethod
    async def get_location_coordinates(city: str) -> dict:
        params = {"name": city, "count": 1, "format": "json"}

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherService.GEO_URL, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])

            if not results:
                return None

            return {
                "lat": results[0]["latitude"],
                "lon": results[0]["longitude"],
                "name": results[0]["name"],
                "country": results[0]["country"],
            }

    @staticmethod
    async def get_weather(latitude: float, longitude: float) -> WeatherInfo:
        """Get current weather coordinates."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "uv_index_max",
            ],
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "weather_code",
                "wind_speed_10m",
                "apparent_temperature",
            ],
            "timezone": "auto",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherService.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        current = data["current"]
        daily = data["daily"]

        weather_code = current.get("weather_code", 0)
        icon, conditions = WeatherService._map_weather_code(weather_code)
        full_conditions = f"{icon} {conditions}"

        uv_max = daily.get("uv_index_max", [0])[0]
        needs_sunscreen = uv_max >= 3.0

        RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}
        rain_chance = daily.get("precipitation_probability_max", [0])[0]
        needs_umbrella = weather_code in RAIN_CODES or rain_chance > 30

        return WeatherInfo(
            temperature_celsius=current["temperature_2m"],
            conditions=full_conditions,
            precipitation_chance=rain_chance,
            humidity=current["relative_humidity_2m"],
            wind_speed_kmh=current["wind_speed_10m"],
            feels_like_celsius=current["apparent_temperature"],
            needs_umbrella=needs_umbrella,
            daily_max_temperature=daily["temperature_2m_max"][0],
            daily_min_temperature=daily["temperature_2m_min"][0],
            uv_index=uv_max,
            needs_sunscreen=needs_sunscreen,
        )

    @staticmethod
    def _map_weather_code(code: int) -> str:
        """Mapping WMO weather codes to simple conditions"""
        mapping = {
            # Clear & Clouds
            0: ("☀️", "Clear sky"),
            1: ("🌤️", "Mainly clear"),
            2: ("⛅", "Partly cloudy"),
            3: ("☁️", "Overcast"),
            # Fog
            45: ("🌫️", "Fog"),
            48: ("🌫️", "Depositing rime fog"),
            # Drizzle
            51: ("🌦️", "Light drizzle"),
            53: ("🌦️", "Moderate drizzle"),
            55: ("🌦️", "Dense drizzle"),
            56: ("🌧️", "Light freezing drizzle"),
            57: ("🌧️", "Dense freezing drizzle"),
            # Rain
            61: ("🌧️", "Slight rain"),
            63: ("🌧️", "Moderate rain"),
            65: ("🌧️", "Heavy rain"),
            66: ("❄️", "Light freezing rain"),
            67: ("❄️", "Heavy freezing rain"),
            # Snow
            71: ("❄️", "Slight snow fall"),
            73: ("❄️", "Moderate snow fall"),
            75: ("❄️", "Heavy snow fall"),
            77: ("🌨️", "Snow grains"),
            # Showers
            80: ("🌦️", "Slight rain showers"),
            81: ("🌧️", "Moderate rain showers"),
            82: ("⛈️", "Violent rain showers"),
            85: ("🌨️", "Slight snow showers"),
            86: ("🌨️", "Heavy snow showers"),
            # Thunderstorms
            95: ("⛈️", "Thunderstorm"),
            96: ("⛈️", "Thunderstorm with slight hail"),
            99: ("⛈️", "Thunderstorm with heavy hail"),
        }
        return mapping.get(code, ("❓", f"Unknown (Code {code})"))
