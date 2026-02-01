import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

def get_backend_health():
    try:
        response = requests.get(f"{BACKEND_URL}/health/", timeout=2)
        if response.status_code == 200:
            return response.json()
        return {"status": "unhealthy", "detail": "Non-200 response"}
    except requests.RequestException as e:
        return {"status": "unhealthy", "detail": str(e)}