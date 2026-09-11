"""Geocoding Service for ClimateEye AI.

Uses Open-Meteo Geocoding API to resolve location names into geographic coordinates
and administrative metadata dynamically without hardcoded datasets.
"""

from typing import Any, Dict, List
import httpx


class GeocodingService:
    """Service to resolve place names to geographical coordinates and regional details."""

    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    async def search_location(self, query: str, count: int = 5) -> List[Dict[str, Any]]:
        """Search for locations matching a query string.

        Args:
            query: The search term (city, region, place name).
            count: Maximum number of results to return (default 5).

        Returns:
            List of parsed location results with lat, lon, city, region, country.
        """
        if not query or not query.strip():
            return []

        params = {
            "name": query.strip(),
            "count": count,
            "language": "en",
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        raw_results = data.get("results", [])
        parsed_results = []

        for item in raw_results:
            parsed_results.append({
                "id": item.get("id"),
                "city": item.get("name"),
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "country": item.get("country"),
                "country_code": item.get("country_code"),
                "state_or_region": item.get("admin1"),
                "timezone": item.get("timezone"),
            })

        return parsed_results


geocoding_service = GeocodingService()
