# SkyRide Weather API

A full-stack weather application designed to provide real-time hyperlocal weather data for urban bike courier operations. The backend uses FastAPI to orchestrate geocoding and weather APIs, while the frontend offers an intuitive dispatch-focused interface for weather monitoring.

## 🎯 Project Overview

SkyRide keeps urban logistics teams informed and protected with at-a-glance weather insights and dispatch-ready route planning. The application integrates real-time geocoding and weather data to support high-volume delivery operations across multiple cities.

### Key Features

**Backend API**
- City-to-coordinates geocoding via Geoapify API
- Real-time weather data fetching from OpenWeather API
- Structured response formatting with comprehensive weather metrics
- CORS-enabled for seamless frontend integration
- Comprehensive logging for debugging and monitoring

**Frontend Interface**
- Modern, responsive UI built with vanilla HTML/CSS/JavaScript
- City search with quick lookup or saved city selection
- Real-time weather card generation with dispatch-ready details
- Mobile-optimized design for field operations
- Temperature, wind, visibility, humidity, and pressure monitoring

## 🛠️ Tech Stack

**Backend**
- Python 3.x
- FastAPI (modern async web framework)
- Requests (HTTP client for API calls)
- Uvicorn (ASGI server)
- python-dotenv (environment variable management)

**Frontend**
- HTML5 / CSS3 (modern responsive design)
- Vanilla JavaScript (no frameworks)
- Geoapify Geocoding API
- OpenWeather API

**APIs**
- [Geoapify Geocoding API](https://www.geoapify.com/) - Convert city names to coordinates
- [OpenWeather API](https://openweathermap.org/api) - Real-time weather data

## 📋 Prerequisites

- Python 3.8+
- Modern web browser
- API keys for both Geoapify and OpenWeather

## ⚙️ Installation & Setup

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd skyride-weather-api
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with your API keys:

```env
GEOCODING_API_KEY=your_geoapify_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

**Getting API Keys:**

- **Geoapify**: Sign up at [geoapify.com](https://www.geoapify.com/) and generate a free API key
- **OpenWeather**: Sign up at [openweathermap.org](https://openweathermap.org/api) and generate a free API key

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually install required packages:

```bash
pip install fastapi uvicorn requests python-dotenv
```

### 4. Run the Backend Server

```bash
python app.py
```

The API will start on `http://localhost:8000`

You'll see startup output like:

```
🚀 Starting SkyRide Weather API...

==================================================
APP STARTUP DEBUG
==================================================
✓ GEOCODING_API_KEY loaded: True
✓ OPENWEATHER_API_KEY loaded: True
==================================================
```

### 5. Open the Frontend

Open `index.html` in your web browser (double-click or drag into browser window).

## 📡 API Endpoints

### Health Check

**GET** `/`

Returns backend status.

**Response:**
```json
{
  "message": "Hello World",
  "status": "Backend is running"
}
```

### Weather Query

**GET** `/weather?city={city_name}`

Fetches weather data for a specified city.

**Parameters:**
- `city` (string, required): City name (e.g., "Boston", "New York")

**Response:**
```json
{
  "input_city": "Boston",
  "city": "Boston",
  "country": "US",
  "coordinates": {
    "lat": 42.3601,
    "lon": -71.0589
  },
  "conditions": {
    "label": "Clear",
    "description": "clear sky",
    "icon": "01d"
  },
  "temperature": {
    "current_c": 12.5,
    "feels_like_c": 10.2,
    "min_c": 10.1,
    "max_c": 14.8
  },
  "humidity": 65,
  "pressure": 1013,
  "wind": {
    "speed_mps": 3.5,
    "direction_deg": 240,
    "gust_mps": 5.2
  },
  "visibility_m": 10000,
  "cloud_cover_pct": 10,
  "timestamp": 1704067200,
  "timezone_offset_s": -18000,
  "source": "openweathermap"
}
```

## 🔧 Project Structure

```
skyride-weather-api/
├── app.py              # FastAPI backend with all endpoints and integrations
├── index.html          # Frontend UI for weather queries and display
├── .env                # Environment variables (create this file)
└── README.md           # This file
```

## 🚀 Usage Guide

### Using the Frontend

1. **Quick City Search**: Type any city name in the search field (e.g., "Chicago", "London")
2. **Saved Cities**: Select from pre-loaded cities in the dropdown (New York, Philadelphia, Chicago, Los Angeles)
3. **Submit**: Click "Check Weather" or press Enter to fetch live data
4. **View Results**: Weather card displays all key metrics for dispatch planning

### Using the API Directly

Query the API from any HTTP client (curl, Postman, etc.):

```bash
curl "http://localhost:8000/weather?city=Boston"
```

## 🔍 Key Functions

### Backend (`app.py`)

**`convert_cityname_to_coordinate(city)`**
- Converts city names to geographic coordinates
- Uses Geoapify Geocoding API
- Includes error handling for unknown cities

**`weather_info(lat, lon)`**
- Fetches current weather data
- Uses OpenWeather API with lat/lon coordinates
- Returns raw JSON payload

**`formatter(payload)`**
- Transforms raw API response into user-friendly format
- Converts temperature from Kelvin to Celsius
- Extracts and organizes weather metrics
- Returns structured weather object

### Frontend (`index.html`)

**`fetchWeather(city)`**
- Makes async request to backend `/weather` endpoint
- Handles loading states and error messages
- Renders weather card with results

**`renderWeatherCard(data)`**
- Creates DOM elements for weather display
- Formats wind speed, visibility, temperature ranges
- Updates dispatch-focused information

**`toggleSubmitState()`**
- Enables/disables submit button based on input
- Improves UX with intelligent state management

## 🧪 Testing

### Test Backend Endpoints

```bash
# Test health check
curl http://localhost:8000/

# Test weather endpoint
curl "http://localhost:8000/weather?city=New%20York"

# Test with special characters
curl "http://localhost:8000/weather?city=São%20Paulo"
```

### Debug Mode

The app includes comprehensive logging output. Monitor the terminal where you started `app.py` to see:

- API key loading status on startup
- Geocoding requests and coordinate results
- Weather API calls and responses
- Data formatting operations
- Error traces for troubleshooting

Example debug output:

```
==================================================
[WEATHER REQUEST] City: Boston
==================================================
[GEOCODING] Fetching coordinates for: Boston
[GEOCODING] ✓ Found: Boston at (42.3601, -71.0589)
[WEATHER] Fetching weather for coordinates: (42.3601, -71.0589)
[WEATHER] ✓ Received weather data
[FORMATTER] ✓ Formatted weather data for Boston
[SUCCESS] Weather data returned for Boston
==================================================
```

## 🚨 Troubleshooting

### Missing API Keys Error

**Error Message**: `WARNING: Missing API keys in .env file!`

**Solution**: Ensure your `.env` file exists with both API keys properly set.

### City Not Found

**Error**: `City 'InvalidCity' not found in geocoding results`

**Solution**: Double-check city spelling or use major city names.

### Connection Refused

**Error**: `Connection refused at localhost:8000`

**Solution**: Ensure backend is running with `python app.py`

### CORS Errors

The backend is configured to accept requests from any origin (`allow_origins=["*"]`). If CORS issues persist, check that both frontend and backend are running.

### Request Timeout

**Error**: `Request timed out (5 seconds)`

**Cause**: API service unavailable or network issue

**Solution**: Check internet connection and verify API services are online.

## 🌐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEOCODING_API_KEY` | Geoapify API key for geocoding | `abc123xyz789` |
| `OPENWEATHER_API_KEY` | OpenWeather API key | `def456uvw012` |

## 📦 Requirements File

Create `requirements.txt` for easy dependency installation:

```
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
python-dotenv==1.0.0
```

## 🎨 Design Philosophy

**Backend**: Clean separation of concerns with dedicated functions for geocoding, weather fetching, and formatting. Comprehensive error handling and logging for operational visibility.

**Frontend**: Dispatch-focused interface emphasizing actionable weather metrics (wind speed, visibility, temperature ranges) relevant to courier operations. Responsive design ensures usability on tablets and mobile devices in the field.

## 🔮 Future Enhancements

- Multi-city batch queries for regional dispatch coverage
- Geofencing for automatic zone weather updates
- Weather alerts and notifications for hazardous conditions
- Historical weather data for route optimization
- Integration with routing APIs for ETA adjustments
- User authentication and dispatch team management
- Mobile app for iOS/Android

## 📝 API Response Codes

- `200`: Success
- `400`: Bad request (invalid city parameter)
- `500`: Server error (API key issues, API failures, data formatting errors)

## 🤝 Contributing

To extend this project:

1. Add new weather metrics to the `formatter()` function
2. Implement additional geocoding providers in `convert_cityname_to_coordinate()`
3. Create new frontend views for different dispatch workflows
4. Add authentication for multi-user scenarios

## 📄 License

This project is provided as-is for educational and operational use.

## ✉️ Support & Documentation

For detailed API documentation, run the server and visit: `http://localhost:8000/docs` (FastAPI auto-generated Swagger UI)

---

**Built for dispatch teams who need real-time weather intelligence.** 🚴‍♂️💨