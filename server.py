import os
from flask import Flask, request, jsonify, send_from_directory
from services.weather_service import fetch_weather
from services.geocoding_service import reverse_geocode, search_locations
from services.chat_service import generate_chat_response

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "ClimateEYE Intelligence Platform",
        "version": "3.1.0",
        "features": ["geolocation", "reverse_geocoding", "forward_search", "open_meteo_weather", "ai_chatbot"]
    })

def extract_coords(req):
    """Extract and validate latitude and longitude from request."""
    if req.method == "POST":
        data = req.get_json(silent=True) or {}
        lat_raw = data.get("latitude") if "latitude" in data else data.get("lat")
        lon_raw = data.get("longitude") if "longitude" in data else data.get("lon")
    else:
        lat_raw = req.args.get("latitude") or req.args.get("lat")
        lon_raw = req.args.get("longitude") or req.args.get("lon")

    if lat_raw is None or lon_raw is None:
        raise ValueError("Missing coordinates. Both 'latitude' and 'longitude' are required.")

    try:
        lat = float(lat_raw)
        lon = float(lon_raw)
    except (ValueError, TypeError):
        raise ValueError(f"Coordinates must be valid decimal numbers. Received latitude='{lat_raw}', longitude='{lon_raw}'.")

    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"Invalid latitude: {lat}. Latitude must be between -90.0 and +90.0 degrees.")

    if not (-180.0 <= lon <= 180.0):
        raise ValueError(f"Invalid longitude: {lon}. Longitude must be between -180.0 and +180.0 degrees.")

    return lat, lon

@app.route("/api/search-locations", methods=["GET"])
def handle_search_locations():
    """
    Forward-geocoding search API:
    Dynamically converts city/place name queries into coordinates.
    Zero hardcoded city lists.
    """
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({
            "status": "error",
            "message": "Query parameter 'q' is required."
        }), 400

    limit = request.args.get("limit", 6)
    try:
        limit = int(limit)
    except ValueError:
        limit = 6

    results = search_locations(query, limit=limit)
    return jsonify({
        "status": "success",
        "query": query,
        "count": len(results),
        "results": results
    }), 200

@app.route("/api/reverse-geocode", methods=["POST", "GET"])
def handle_reverse_geocode():
    try:
        lat, lon = extract_coords(request)
        data = reverse_geocode(lat, lon)
        return jsonify({
            "status": "success",
            "data": data
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "error_type": "INVALID_COORDINATES",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_type": "GEOCODING_ERROR",
            "message": f"Reverse-geocoding failed: {str(e)}"
        }), 500

@app.route("/api/weather", methods=["POST", "GET"])
def handle_weather():
    """
    Fetch real-time weather metrics from Open-Meteo via backend service layer.
    """
    try:
        lat, lon = extract_coords(request)
        weather_data = fetch_weather(lat, lon)
        return jsonify({
            "status": "success",
            "data": weather_data
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "error_type": "INVALID_COORDINATES",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_type": "WEATHER_FETCH_ERROR",
            "message": f"Failed to retrieve weather data: {str(e)}"
        }), 502

@app.route("/api/climate-snapshot", methods=["POST", "GET"])
def handle_climate_snapshot():
    """Combined endpoint returning both reverse-geocoded location and live weather."""
    try:
        lat, lon = extract_coords(request)
        location_data = reverse_geocode(lat, lon)
        weather_data = fetch_weather(lat, lon)
        return jsonify({
            "status": "success",
            "data": {
                "location": location_data,
                "weather": weather_data
            }
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "error_type": "INVALID_COORDINATES",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_type": "SNAPSHOT_ERROR",
            "message": f"Snapshot failed: {str(e)}"
        }), 500

@app.route("/api/chat", methods=["POST"])
def handle_chat():
    """
    AI Climate Assistant endpoint:
    Answers user queries with live location and weather context.
    """
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    context = payload.get("context", {})

    reply = generate_chat_response(message, context)
    return jsonify({
        "status": "success",
        "reply": reply
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting ClimateEYE Server on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)
