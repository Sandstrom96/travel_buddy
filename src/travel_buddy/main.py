from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from travel_buddy.api.router import router as main_router

app = FastAPI(
    title="Travel Buddy API",
    description="AI-powered travel guide",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Konnichiwa! Welcome to the Travel Buddy Japan API.",
        "docs": "/docs",
    }
