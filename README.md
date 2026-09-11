# ClimateEYE AI — Atmospheric Intelligence & Climate Assistant

ClimateEYE AI is a modern environmental intelligence platform integrating browser Geolocation, Open-Meteo real-time atmospheric telemetry, dynamic global city search, and a context-aware AI climate assistant.

## Key Features

- 📍 **Browser Geolocation**: Instant regional detection using the HTML5 Geolocation API with high-accuracy GPS and robust error handling.
- 🔍 **Dynamic Global City Search**: Forward-geocoding supporting any city worldwide (Ahmedabad, Surat, Mumbai, Delhi, etc.) with zero hardcoded lists.
- ⛅ **Real-Time Open-Meteo Integration**: Fetches and renders live atmospheric parameters:
  - Ambient Temperature
  - Apparent / Feels-Like Temperature
  - Relative Humidity
  - Cloud Cover
  - Precipitation Accumulation
  - Wind Speed
  - WMO Weather Condition translation
- 🗺️ **Interactive Radar Map**: Embedded Leaflet.js map centering on detected observation coordinates.
- 🤖 **Context-Aware AI Assistant**: Synchronized chatbot that answers questions based on the active location and live climate parameters.

## Architecture

```
ClimateEYE_ai_code/
├── server.py                   # Flask backend with search, weather, and chat endpoints
├── index.html                  # Semantic dashboard layout and chatbot UI
├── services/
│   ├── weather_service.py      # Open-Meteo forecast client & WMO code mapper
│   ├── geocoding_service.py    # Forward and reverse geocoding services
│   └── chat_service.py         # Context-aware AI assistant responses
└── static/
    ├── css/style.css           # Glassmorphic climate-tech design system
    └── js/app.js               # Frontend application logic and state sync
```

## Running the Project

1. Install Python dependencies:
   ```bash
   pip install flask requests dulwich
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Open `http://127.0.0.1:5000` in your web browser.
