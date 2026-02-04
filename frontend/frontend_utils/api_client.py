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
    

def send_chat_message(query: str, thread_id: str = None):
    
    payload = {"query": query, "thread_id": thread_id}

    try:
        response = requests.post(f"{BACKEND_URL}/agent/chat", json=payload, timeout=30)

        if response.status_code == 200:
            return response.json().get("response", "Inget svar från AI-hjärnan.")
        else:
            return f"Servern svarade med statuskod: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Kunde inte ansluta till backend. är servern igång?"
    except Exception as e:
        return f"Ett okänt fel uppstod: {e}"
