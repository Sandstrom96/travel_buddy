import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class APIClient:
    @staticmethod
    def get_health():
        try:
            response = requests.get(f"{BACKEND_URL}/health/", timeout=2)
            return response.json()
        except:
            return {"status": "offline"}

    @staticmethod
    def get_recommendations(user_lat: float, user_lon: float, activity_type: str = "ice_cream", max_results: int = 5):
        payload = {
            "user_latitude": user_lat,
            "user_longitude": user_lon,
            "activity_type": activity_type,
            "max_results": max_results
        }
        try:
            response = requests.post(f"{BACKEND_URL}/recommendations/", json=payload, timeout=10)
            return response.json() if response.status_code == 200 else []
        except:
            return []

def send_chat_message(query: str, country: str, history: list = None):
    payload = {"query": query, "country": country.lower(), "history": history or []}
    try:
        response = requests.post(f"{BACKEND_URL}/agent/chat", json=payload, timeout=30)
        return response.json() if response.status_code == 200 else {"response": "Error", "history": history}
    except Exception as e:
        return {"response": str(e), "history": history}

def get_backend_health():
    return APIClient.get_health()