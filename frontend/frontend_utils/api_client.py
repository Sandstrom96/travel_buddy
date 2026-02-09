import requests
import os


BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


class APIClient:
    # För att hålla recommendations.py nöjd(inte krascha).
    @staticmethod
    def get_health():
        try:
            response = requests.get(f"{BACKEND_URL}/health/", timeout=2)
            return response.json()
        except:
            return {"status": "unhealthy"}

    @staticmethod
    def get_recommendations(
        user_lat: float,
        user_lon: float,
        activity_type: str = "ice_cream",
        max_results: int = 5,
    ):
        sanitized_activity = activity_type.lower().replace(" ", "_")
        payload = {
            "user_latitude": user_lat,
            "user_longitude": user_lon,
            "activity_type": sanitized_activity,
            "max_results": max_results,
        }
        try:
            response = requests.post(
                f"{BACKEND_URL}/recommendations/", json=payload, timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []

        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []
    
    @staticmethod 
    def get_airports(city: str):
        try:
            response = requests.get(f"{BACKEND_URL}/transport/airports/{city}", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Error fetching airports: {e}")
            return []
    
    @staticmethod
    def get_hotels_areas(city: str):
        try:
            response = requests.get(f"{BACKEND_URL}/transport/hotels/{city}", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Error fetching hotel areas: {e}")
            return []
    
    @staticmethod
    def get_transport_route(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float):
        try:
            payload = {
                "origin_lat": origin_lat,
                "origin_lon": origin_lon,
                "dest_lat": dest_lat,
                "dest_lon": dest_lon
            }
            response = requests.post(f"{BACKEND_URL}/transport/route", json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Error calculating route: {e}")
            return []



# healthcheck
def get_backend_health():
    return APIClient.get_health()


def send_chat_message(query: str, country: str, history: list = None):

    payload = {
        "query": query,
        "country": country.lower(),
        "history": history or [],
    }

    try:
        response = requests.post(f"{BACKEND_URL}/agent/chat", json=payload, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "response": f"Servern svarade med statuskod: {response.status_code}",
                "history": history or [],
            }
    except Exception as e:
        return {"response": f"Ett okänt fel uppstod: {e}", "history": history or []}


