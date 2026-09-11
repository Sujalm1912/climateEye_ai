"""Location API Route.

Endpoint for searching locations and resolving geographic coordinates.
"""

from typing import Optional
from fastapi import APIRouter, Query

from app.services.geocoding_service import geocoding_service

router = APIRouter(prefix="/api/location", tags=["Location"])


@router.get("/search")
async def search_location(
    q: Optional[str] = Query(None, min_length=1, description="Location search term (e.g., city or region)"),
):
    """Search for locations using Open-Meteo Geocoding API.

    In this initial phase, returns a placeholder response indicating service readiness.
    If a search term `q` is provided, it previews dynamic geocoding.
    """
    if q and q.strip():
        try:
            results = await geocoding_service.search_location(q.strip())
            return {
                "status": "ok",
                "message": f"Found {len(results)} location(s)",
                "data": results,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Geocoding lookup failed: {str(e)}",
            }

    return {
        "status": "not implemented yet",
        "message": "Location search endpoint ready for Open-Meteo Geocoding. Provide ?q=city_name to search.",
    }
