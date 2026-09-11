# ClimateEye AI

> **"See Earth through data. Understand it through AI."**

ClimateEye AI is an AI-powered environmental intelligence platform designed to deliver real-time meteorological insight, climate risk awareness, and conversational intelligence for any location on Earth.

---

## 1. What ClimateEye AI Is

ClimateEye AI empowers individuals, researchers, and climate advocates to observe planetary conditions through transparent data and understand them through contextual AI. 

In its complete vision, users will be able to:
1. Detect their current location or search for any global place.
2. Retrieve real-time, high-precision weather and environmental indicators (temperature, humidity, precipitation, wind dynamics, cloud cover, and severe condition warnings).
3. Chat with an AI assistant specifically grounded in localized environmental datasets.
4. Analyze historical climate trends and anomaly shifts.
5. Ingest Earth observation and satellite data for deep geospatial insights.

---

## 2. Project Architecture

The application enforces a decoupled full-stack architecture where frontend client code and backend business logic are strictly separated:

```
                      ┌────────────────────────────────┐
                      │          User Client           │
                      └───────────────┬────────────────┘
                                      │
                                      ▼
                      ┌────────────────────────────────┐
                      │    React + Vite + TypeScript   │
                      │         (Frontend UI)          │
                      └───────────────┬────────────────┘
                                      │ HTTP / REST
                                      ▼
                      ┌────────────────────────────────┐
                      │       FastAPI Backend          │
                      │       (Python + ASGI)          │
                      └───────┬───────────────┬────────┘
                              │               │
            ┌─────────────────┴────┐     ┌────┴─────────────────┐
            │                      │     │                      │
            ▼                      ▼     ▼                      ▼
┌───────────────────────┐ ┌────────────┐ ┌────────────────────────┐
│   Geocoding Service   │ │ Weather    │ │   Gemini AI Service    │
│   (Open-Meteo API)    │ │ Service    │ │   (google-genai SDK)   │
└───────────────────────┘ └────────────┘ └────────────────────────┘
            │                      │                    │
            └───────────┬──────────┘                    │
                        ▼                               ▼
            ┌────────────────────────┐      ┌───────────────────────┐
            │   External Weather &   │      │   Google AI Studio    │
            │     Geocoding APIs     │      │      Gemini API       │
            └────────────────────────┘      └───────────────────────┘
```

---

## 3. Technologies Used

### Frontend
- **React (v18+)**: Component-driven UI rendering.
- **Vite**: Rapid, modern frontend build tool and dev server.
- **TypeScript**: Static typing for maintainable, type-safe development.
- **Modern CSS**: Vanilla CSS design system with dark-mode aesthetic and glassmorphism.

### Backend
- **FastAPI**: Modern, high-performance web framework for building APIs with Python.
- **Uvicorn**: Lightning-fast ASGI web server.
- **google-genai**: Google's official, current Python SDK for Gemini models.
- **Open-Meteo**: Free, open meteorological and geocoding APIs (no API keys required).
- **HTTPX**: Modern async HTTP client for external service integration.
- **python-dotenv**: Environment variable management.

---

## 4. Folder Structure

```
ClimateEye_AI/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py           # /api/chat endpoint
│   │   │   ├── location.py       # /api/location/search endpoint
│   │   │   └── weather.py        # /api/weather endpoint
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── gemini_service.py # Gemini AI client & generation logic
│   │   │   ├── geocoding_service.py # Open-Meteo Geocoding
│   │   │   └── weather_service.py   # Open-Meteo Weather data fetching
│   │   ├── __init__.py
│   │   └── main.py               # FastAPI entry point & CORS configuration
│   ├── .env.example              # Template for environment variables
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   │   ├── api.ts            # Base HTTP client with error handling
│   │   │   ├── chatService.ts    # Frontend chat API bridge
│   │   │   ├── locationService.ts# Frontend location API bridge
│   │   │   └── weatherService.ts # Frontend weather API bridge
│   │   ├── App.tsx               # Main application component
│   │   ├── index.css             # Dark-mode environmental styling
│   │   └── main.tsx              # React mounting point
│   ├── index.html                # HTML template with Google Fonts
│   ├── package.json              # Node.js dependencies and scripts
│   ├── tsconfig.json             # TypeScript configuration
│   └── vite.config.ts            # Vite dev server and proxy setup
├── .gitignore                    # Git ignore rules for secrets and builds
└── README.md                     # Project documentation
```

---

## 5. Installation Requirements

Make sure the following runtimes are installed on your system:
- **Python**: Version 3.10 or newer (tested with Python 3.14).
- **Node.js**: Version 18 or newer (tested with Node.js LTS v24 / npm v11).
- **Git**: For version control.

---

## 6. How to Create the Python Virtual Environment

From the project root directory (`ClimateEye_AI`):

### Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

*(When active, you will see `(.venv)` displayed at the start of your terminal line).*

---

## 7. How to Install Backend Dependencies

With the virtual environment activated, install the required packages:

```powershell
pip install -r backend/requirements.txt
```

---

## 8. How to Install Frontend Dependencies

Open a new terminal or navigate to the `frontend` folder to install npm packages:

```powershell
cd frontend
npm install
cd ..
```

Or from the project root:
```powershell
npm --prefix frontend install
```

---

## 9. How to Configure `.env`

Create a private `.env` file inside `backend/`:

1. Copy the template:
   ```powershell
   copy backend\.env.example backend\.env
   ```
2. Open `backend/.env` in an editor.
3. Obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).
4. Add your key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

> **Security Note**: Never commit `backend/.env` to Git. It is already included in `.gitignore`. Never expose your Gemini API key inside frontend code.

---

## 10. How to Start the Backend

From the project root with the virtual environment activated:

```powershell
uvicorn backend.app.main:app --reload --port 8000
```

The FastAPI server will be accessible at:
- API Base: `http://127.0.0.1:8000`
- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/health`

---

## 11. How to Start the Frontend

From the project root:

```powershell
npm --prefix frontend run dev
```

The React + Vite application will be available at:
- Web App: `http://localhost:5173`

The frontend includes an automated health badge that connects to `http://127.0.0.1:8000/health` and verifies that the backend is online.

---

## 12. Available API Routes

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root endpoint displaying service identity. |
| `GET` | `/health` | Diagnostic health check returning service name and version. |
| `GET` | `/api/weather` | Retrieve weather metrics (accepts `?latitude=&longitude=`). |
| `GET` | `/api/location/search` | Dynamic geocoding lookup (accepts `?q=city_name`). |
| `POST` | `/api/chat` | Environmental intelligence conversational endpoint. |

---

## 13. Planned Development Phases

- **Phase 1 (Current)**: Development environment, separate React + FastAPI architecture, service contracts, and security practices.
- **Phase 2**: Real-time location search and interactive Open-Meteo weather dashboard.
- **Phase 3**: Environmental intelligence chatbot powered by Google Gemini and real-time climate context.
- **Phase 4**: Historical climate trends and anomaly analysis.
- **Phase 5**: Earth observation / satellite data integration.
