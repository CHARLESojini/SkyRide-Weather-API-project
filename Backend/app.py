import requests
import os
from dotenv import load_dotenv
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()

geo_api_key = os.getenv('GEOCODING_API_KEY')
weather_apikey = os.getenv('OPENWEATHER_API_KEY')

# Debug: Print API keys status on startup
print("=" * 50)
print("APP STARTUP DEBUG")
print("=" * 50)
print(f"✓ GEOCODING_API_KEY loaded: {bool(geo_api_key)}")
print(f"✓ OPENWEATHER_API_KEY loaded: {bool(weather_apikey)}")
if not geo_api_key or not weather_apikey:
    print("⚠️  WARNING: Missing API keys in .env file!")
    print("   Create a .env file with:")
    print("   GEOCODING_API_KEY=your_key")
    print("   OPENWEATHER_API_KEY=your_key")
print("=" * 50)

# Helper function
def convert_kelvin_to_celsius(value: float):
    return round(value - 273.15, 1)

# Geocoding API
def convert_cityname_to_coordinate(city):
    """Convert city name to latitude and longitude"""
    try:
        url = f"https://api.geoapify.com/v1/geocode/search?text={city}&format=json&apiKey={geo_api_key}"
        print(f"[GEOCODING] Fetching coordinates for: {city}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        if not data.get('results') or len(data['results']) == 0:
            raise ValueError(f"City '{city}' not found in geocoding results")
        
        lon = data['results'][0]['lon']
        lat = data['results'][0]['lat']
        print(f"[GEOCODING] ✓ Found: {city} at ({lat}, {lon})")
        return lat, lon
    except requests.exceptions.RequestException as e:
        print(f"[GEOCODING] ✗ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Geocoding API error: {str(e)}. Check GEOCODING_API_KEY."
        )
    except Exception as e:
        print(f"[GEOCODING] ✗ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def weather_info(lat, lon):
    """Fetch weather data from OpenWeather API"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_apikey}"
        print(f"[WEATHER] Fetching weather for coordinates: ({lat}, {lon})")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"[WEATHER] ✓ Received weather data")
        return data
    except requests.exceptions.RequestException as e:
        print(f"[WEATHER] ✗ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Weather API error: {str(e)}. Check OPENWEATHER_API_KEY."
        )
    except Exception as e:
        print(f"[WEATHER] ✗ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def formatter(payload: dict[str, Any]):
    """Format raw weather data into readable format"""
    try:
        weather = payload.get("weather", [{}])[0]
        main = payload.get("main", {})
        wind = payload.get("wind", {})

        formatted = {
            "city": payload.get("name"),
            "country": payload.get("sys", {}).get("country"),
            "coordinates": payload.get("coord"),
            "conditions": {
                "label": weather.get("main"),
                "description": weather.get("description"),
                "icon": weather.get("icon"),
            },
            "temperature": {
                "current_c": convert_kelvin_to_celsius(main.get("temp", 0)),
                "feels_like_c": convert_kelvin_to_celsius(main.get("feels_like", 0)),
                "min_c": convert_kelvin_to_celsius(main.get("temp_min", 0)),
                "max_c": convert_kelvin_to_celsius(main.get("temp_max", 0)),
            },
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "wind": {
                "speed_mps": wind.get("speed"),
                "direction_deg": wind.get("deg"),
                "gust_mps": wind.get("gust"),
            },
            "visibility_m": payload.get("visibility"),
            "cloud_cover_pct": payload.get("clouds", {}).get("all"),
            "timestamp": payload.get("dt"),
            "timezone_offset_s": payload.get("timezone"),
            "source": "openweathermap",
        }
        print(f"[FORMATTER] ✓ Formatted weather data for {formatted['city']}")
        return formatted
    except Exception as e:
        print(f"[FORMATTER] ✗ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data formatting error: {str(e)}")

# CORS Middleware - MUST be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Health check endpoint"""
    print("[ROOT] Health check request")
    return {"message": "Hello World", "status": "Backend is running"}

@app.get("/weather")
def weather(city: str):
    """Main weather endpoint - takes city name and returns formatted weather data"""
    try:
        print(f"\n{'='*50}")
        print(f"[WEATHER REQUEST] City: {city}")
        print(f"{'='*50}")
        
        # Step 1: Convert city to coordinates
        lat, lon = convert_cityname_to_coordinate(city)
        
        # Step 2: Get weather data
        payload = weather_info(lat, lon)
        
        # Step 3: Format response
        formatted_data = formatter(payload)
        formatted_data['input_city'] = city
        
        print(f"[SUCCESS] Weather data returned for {city}")
        print(f"{'='*50}\n")
        return formatted_data
        
    except HTTPException:
        raise  # Re-raise FastAPI exceptions
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        print(f"{'='*50}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting SkyRide Weather API...\n")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)