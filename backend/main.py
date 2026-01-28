""" Main module for Travel Buddy API. Connects all endpoints and starts the server."""

from fastapi import FastAPI
from endpoints import (
    health,
    destinations,
    agent,
    guide,
)

app = FastAPI(title="Travel Buddy Japan API")
app.include_router(health.router, prefix="/health", tags = ["Health"])
app.include_router(destinations.router, prefix="/destinations", tags = ["Japan Destinations"])
app.include_router(agent.router, prefix="/agent", tags = ["AI TravelAgent"])
app.include_router(guide.router, prefix="/guide", tags = ["Travel Guides"])


app.get("/")
async def root():
    return {"message": "Konnichiwa! Welcome to the Travel Buddy Japan API."}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)