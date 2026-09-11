"""
Weather Service Module for ClimateEYE
Connects directly to Open-Meteo API to fetch real-time atmospheric data.
Translates WMO weather codes to human-readable condition descriptions and icons.
"""

import requests
from datetime import datetime

OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Standard WMO Weather Interpretation Codes (WW)
WMO_CODE_MAP = {
    0: {"condition": "Clear Sky", "icon": "sun", "category": "clear"},
    1: {"condition": "Mainly Clear", "icon": "sun-cloud", "category": "clear"},
    2: {"condition": "Partly Cloudy", "icon": "cloud-sun", "category": "cloudy"},
    3: {"condition": "Overcast", "icon": "cloud", "category": "cloudy"},
    45: {"condition": "Fog", "icon": "fog", "category": "fog"},
    48: {"condition": "Depositing Rime Fog", "icon": "fog", "category": "fog"},
    51: {"condition": "Light Drizzle", "icon": "cloud-drizzle", "category": "drizzle"},
    53: {"condition": "Moderate Drizzle", "icon": "cloud-drizzle", "category": "drizzle"},
    55: {"condition": "Dense Drizzle", "icon": "cloud-drizzle", "category": "drizzle"},
    56: {"condition": "Light Freezing Drizzle", "icon": "cloud-drizzle", "category": "freezing"},
    57: {"condition": "Dense Freezing Drizzle", "icon": "cloud-drizzle", "category": "freezing"},
    61: {"condition": "Slight Rain", "icon": "cloud-rain", "category": "rain"},
    63: {"condition": "Moderate Rain", "icon": "cloud-rain", "category": "rain"},
    65: {"condition": "Heavy Rain", "icon": "cloud-rain", "category": "rain"},
    66: {"condition": "Light Freezing Rain", "icon": "cloud-rain", "category": "freezing"},
    67: {"condition": "Heavy Freezing Rain", "icon": "cloud-rain", "category": "freezing"},
    71: {"condition": "Slight Snow Fall", "icon": "cloud-snow", "category": "snow"},
    73: {"condition": "Moderate Snow Fall", "icon": "cloud-snow", "category": "snow"},
    75: {"condition": "Heavy Snow Fall", "icon": "cloud-snow", "category": "snow"},
    77: {"condition": "Snow Grains", "icon": "cloud-snow", "category": "snow"},
    80: {"condition": "Slight Rain Showers", "icon": "cloud-rain", "category": "showers"},
    81: {"condition": "Moderate Rain Showers", "icon": "cloud-rain", "category": "showers"},
    82: {"condition": "Violent Rain Showers", "icon": "cloud-rain", "category": "showers"},
    85: {"condition": "Slight Snow Showers", "icon": "cloud-snow", "category": "snow"},
    86: {"condition": "Heavy Snow Showers", "icon": "cloud-snow", "category": "snow"},
    95: {"condition": "Thunderstorm", "icon": "cloud-lightning", "category": "thunderstorm"},
    96: {"condition": "Thunderstorm with Slight Hail", "icon": "cloud-lightning", "category": "thunderstorm"},
    99: {"condition": "Thunderstorm with Heavy Hail", "icon": "cloud-lightning", "category": "thunderstorm"}
}

def get_wmo_condition(code):
    """Resolve WMO code into human-readable description and icon category."""
    if code in WMO_CODE_MAP:
        return WMO_CODE_MAP[code]
    return {"condition": f"Weather Code {code}", "icon": "cloud", "category": "unknown"}

def fetch_weather(lat, lon):
    """
    Fetch current atmospheric weather parameters from Open-Meteo API.
    
    Required parameters:
    - temperature (°C)
    - apparent/feels-like temperature (°C)
    - relative humidity (%)
    - cloud cover (%)
    - precipitation (mm)
    - wind speed (km/h)
    - weather condition
    """
    # Coordinate boundary checks
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        raise ValueError("Latitude and longitude must be valid decimal numbers.")

    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90.0 and +90.0.")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180.0 and +180.0.")

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m",
        "wind_speed_unit": "kmh",
        "timezone": "auto"
    }

    response = requests.get(OPEN_METEO_BASE_URL, params=params, timeout=8)
    if response.status_code != 200:
        raise RuntimeError(f"Open-Meteo API error (HTTP {response.status_code}): {response.text}")

    data = response.json()
    current = data.get("current", {})
    current_units = data.get("current_units", {})

    weather_code = current.get("weather_code", 0)
    wmo_info = get_wmo_condition(weather_code)

    return {
        "latitude": data.get("latitude", lat),
        "longitude": data.get("longitude", lon),
        "elevation": data.get("elevation"),
        "timezone": data.get("timezone", "UTC"),
        "timestamp": current.get("time", datetime.utcnow().isoformat()),
        "temperature": current.get("temperature_2m"),
        "apparent_temperature": current.get("apparent_temperature"),
        "relative_humidity": current.get("relative_humidity_2m"),
        "cloud_cover": current.get("cloud_cover"),
        "precipitation": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "weather_code": weather_code,
        "weather_condition": wmo_info["condition"],
        "weather_icon": wmo_info["icon"],
        "weather_category": wmo_info["category"],
        "units": {
            "temperature": current_units.get("temperature_2m", "°C"),
            "apparent_temperature": current_units.get("apparent_temperature", "°C"),
            "relative_humidity": current_units.get("relative_humidity_2m", "%"),
            "cloud_cover": current_units.get("cloud_cover", "%"),
            "precipitation": current_units.get("precipitation", "mm"),
            "wind_speed": current_units.get("wind_speed_10m", "km/h")
        },
        "source": "Open-Meteo API"
    }
