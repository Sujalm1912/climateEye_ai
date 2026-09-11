"""Weather API Route.

Endpoint for retrieving real-time weather and environmental metrics.
"""

from typing import Optional
from fastapi import APIRouter, Query

from app.services.weather_service import weather_service

router = APIRouter(prefix="/api/weather", tags=["Weather"])


@router.get("")
async def get_weather(
    latitude: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Latitude coordinate"),
    longitude: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Longitude coordinate"),
):
    """Retrieve environmental and weather metrics.

    In this initial phase, returns a placeholder response indicating service readiness.
    If coordinates are supplied, it can preview the underlying Open-Meteo integration.
    """
    if latitude is not None and longitude is not None:
        try:
            weather_data = await weather_service.get_current_weather(latitude, longitude)
            return {
                "status": "ok",
                "message": "Real weather data fetched successfully from Open-Meteo",
                "data": weather_data,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to fetch weather: {str(e)}",
            }

    return {
        "status": "not implemented yet",
        "message": "Weather endpoint ready for Open-Meteo integration. Provide ?latitude=&longitude= to query.",
    }
