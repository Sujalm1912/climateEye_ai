import sys
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.weather import router as weather_router
from app.routes.location import router as location_router
from app.routes.chat import router as chat_router

app = FastAPI(
    title="ClimateEye AI API",
    description="Environmental intelligence backend powered by FastAPI, Open-Meteo, and Google Gemini.",
    version="0.1.0",
)

# Configure CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular route handlers
app.include_router(weather_router)
app.include_router(location_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint for basic service identification."""
    return {
        "status": "ok",
        "service": "ClimateEye AI",
    }


@app.get("/health")
async def health():
    """Health check endpoint for application status and diagnostics."""
    return {
        "status": "ok",
        "service": "ClimateEye AI",
        "version": "0.1.0",
    }
