"""Weather Service for ClimateEye AI.

Integrates with Open-Meteo API (no API key required).
Prepares retrieval of real environmental and meteorological metrics:
- Temperature
- Apparent temperature
- Humidity
- Cloud cover
- Precipitation
- Wind speed
- Wind direction
- Weather condition
"""

from typing import Any, Dict, Optional
import httpx


class WeatherService:
    """Service to fetch real-time weather and environmental metrics from Open-Meteo."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # WMO Weather interpretation codes mapping
    WMO_CODE_MAP = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    def decode_weather_condition(self, weather_code: Optional[int]) -> str:
        """Translate WMO weather code into human-readable description."""
        if weather_code is None:
            return "Unknown"
        return self.WMO_CODE_MAP.get(weather_code, f"Weather code {weather_code}")

    async def get_current_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Fetch current weather metrics for given geographic coordinates.

        Args:
            latitude: Latitude coordinate (-90 to 90).
            longitude: Longitude coordinate (-180 to 180).

        Returns:
            Dictionary containing structured meteorological metrics.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "apparent_temperature",
                "relative_humidity_2m",
                "cloud_cover",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "weather_code",
            ],
            "timezone": "auto",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        current = data.get("current", {})
        weather_code = current.get("weather_code")

        return {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": data.get("timezone"),
            "temperature": current.get("temperature_2m"),
            "apparent_temperature": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "cloud_cover": current.get("cloud_cover"),
            "precipitation": current.get("precipitation"),
            "wind_speed": current.get("wind_speed_10m"),
            "wind_direction": current.get("wind_direction_10m"),
            "weather_condition": self.decode_weather_condition(weather_code),
            "weather_code": weather_code,
            "time": current.get("time"),
        }


weather_service = WeatherService()
