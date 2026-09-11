"""
Geocoding Service Module for ClimateEYE
Provides:
1. Reverse-geocoding (coordinates -> readable location) via BigDataCloud & OSM Nominatim
2. Forward-geocoding (search query -> coordinates) via Open-Meteo Geocoding API with Nominatim fallback
Zero hardcoded city lists: all resolutions are live, dynamic, and global.
"""

import requests

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
BIGDATACLOUD_URL = "https://api.bigdatacloud.net/data/reverse-geocode-client"

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ClimateEYE-App/3.0"
}

def reverse_geocode_bigdatacloud(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "localityLanguage": "en"
    }
    try:
        response = requests.get(BIGDATACLOUD_URL, params=params, timeout=4)
        if response.status_code == 200:
            data = response.json()
            city = data.get("locality") or data.get("city") or ""
            state = data.get("principalSubdivision") or ""
            country = data.get("countryName") or ""

            parts = [p for p in [city, state, country] if p]
            readable_name = ", ".join(parts) if parts else f"{lat:.4f}, {lon:.4f}"

            return {
                "source": "BigDataCloud",
                "display_name": f"{readable_name} ({country})" if country and country not in readable_name else readable_name,
                "readable_name": readable_name,
                "city": city,
                "state": state,
                "country": country,
                "raw_address": data
            }
    except Exception:
        pass
    return None

def reverse_geocode_nominatim(lat, lon):
    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "zoom": 12,
        "addressdetails": 1
    }
    try:
        response = requests.get(NOMINATIM_REVERSE_URL, params=params, headers=HTTP_HEADERS, timeout=4)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("suburb")
                or address.get("municipality")
                or address.get("county")
                or ""
            )
            state = address.get("state") or address.get("region") or ""
            country = address.get("country") or ""

            parts = [p for p in [city, state, country] if p]
            readable_name = ", ".join(parts) if parts else data.get("display_name", f"{lat:.4f}, {lon:.4f}")

            return {
                "source": "OSM Nominatim",
                "display_name": data.get("display_name"),
                "readable_name": readable_name,
                "city": city,
                "state": state,
                "country": country,
                "raw_address": address
            }
    except Exception:
        pass
    return None

def reverse_geocode(lat, lon):
    """Resolve coordinates into human-readable location using tiered providers."""
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        raise ValueError("Latitude and longitude must be valid decimal numbers.")

    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90.0 and +90.0 degrees.")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180.0 and +180.0 degrees.")

    result = reverse_geocode_bigdatacloud(lat, lon)
    if not result:
        result = reverse_geocode_nominatim(lat, lon)

    if not result:
        return {
            "latitude": lat,
            "longitude": lon,
            "readable_name": f"Location ({lat:.4f}°, {lon:.4f}°)",
            "city": "Unknown",
            "state": "Unknown",
            "country": "Unknown",
            "display_name": f"Coordinates: {lat:.6f}, {lon:.6f}",
            "provider": "offline_fallback"
        }

    return {
        "latitude": lat,
        "longitude": lon,
        "readable_name": result["readable_name"],
        "city": result["city"],
        "state": result["state"],
        "country": result["country"],
        "display_name": result["display_name"],
        "provider": result["source"]
    }

def search_locations_open_meteo(query, limit=6):
    """Search forward geocoding using Open-Meteo Geocoding API."""
    params = {
        "name": query,
        "count": min(max(1, limit), 10),
        "language": "en",
        "format": "json"
    }
    response = requests.get(OPEN_METEO_GEOCODING_URL, params=params, timeout=4)
    if response.status_code == 200:
        data = response.json()
        raw_results = data.get("results") or []
        results = []
        for item in raw_results:
            name = item.get("name", "")
            admin1 = item.get("admin1") or item.get("admin2") or ""
            country = item.get("country") or ""
            lat = item.get("latitude")
            lon = item.get("longitude")

            parts = [p for p in [name, admin1, country] if p]
            readable_name = ", ".join(parts) if parts else name

            results.append({
                "name": name,
                "readable_name": readable_name,
                "display_name": f"{readable_name} ({country})",
                "city": name,
                "state": admin1,
                "country": country,
                "latitude": float(lat),
                "longitude": float(lon),
                "provider": "Open-Meteo Geocoding"
            })
        return results
    return []

def search_locations_nominatim(query, limit=6):
    """Search forward geocoding using OSM Nominatim as fallback."""
    params = {
        "q": query,
        "format": "json",
        "limit": min(max(1, limit), 10),
        "addressdetails": 1
    }
    response = requests.get(NOMINATIM_SEARCH_URL, params=params, headers=HTTP_HEADERS, timeout=4)
    if response.status_code == 200:
        raw_items = response.json()
        results = []
        for item in raw_items:
            try:
                lat = float(item.get("lat"))
                lon = float(item.get("lon"))
            except (ValueError, TypeError):
                continue
            address = item.get("address", {})
            city = address.get("city") or address.get("town") or address.get("village") or item.get("display_name", "").split(",")[0].strip()
            state = address.get("state") or ""
            country = address.get("country") or ""
            parts = [p for p in [city, state, country] if p]
            readable_name = ", ".join(parts) if parts else item.get("display_name")
            results.append({
                "name": city,
                "readable_name": readable_name,
                "display_name": item.get("display_name"),
                "city": city,
                "state": state,
                "country": country,
                "latitude": lat,
                "longitude": lon,
                "provider": "OSM Nominatim"
            })
        return results
    return []

def search_locations(query, limit=6):
    """
    Search cities and places dynamically without any hardcoding.
    Tier 1: Open-Meteo Geocoding API (ultra-fast, global)
    Tier 2: OSM Nominatim (detailed address resolution fallback)
    """
    if not query or not query.strip():
        return []

    q = query.strip()
    results = []

    try:
        results = search_locations_open_meteo(q, limit)
    except Exception as e:
        print(f"Open-Meteo Geocoding error: {e}")

    if not results:
        try:
            results = search_locations_nominatim(q, limit)
        except Exception as e:
            print(f"Nominatim Geocoding error: {e}")

    return results
