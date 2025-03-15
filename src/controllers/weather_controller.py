import time
import requests

class WeatherController:
    def __init__(self, google_api_key, openweathermap_api_key):
        self.google_api_key = google_api_key
        self.openweathermap_api_key = openweathermap_api_key
        self.cache = {}  # Cache to store weather data
        self.cache_timeout = 600  # Cache timeout in seconds (10 minutes)

    async def get_user_location(self):
        """Get user location using the Geolocation API."""
        url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.google_api_key
        payload = {"considerIp": "true"}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            location = response.json()
            return location["location"]["lat"], location["location"]["lng"]
        else:
            print("Error fetching location:", response.status_code, response.text)
            return None, None

    async def get_air_quality(self, lat, lng):
        """Fetch air quality data using Google Air Quality API."""
        url = "https://airquality.googleapis.com/v1/currentConditions:lookup"
        payload = {
            "location": {
                "latitude": lat,
                "longitude": lng
            },
            "languageCode": "en"
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{url}?key={self.google_api_key}", json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching air quality data:", response.status_code, response.text)
            return None

    async def get_weather_data(self, lat, lng):
        """Fetch weather data using OpenWeatherMap One Call API."""
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lng}&exclude=hourly,daily&appid={self.openweathermap_api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching weather data:", response.status_code, response.text)
            return None

    async def fetch_weather_data(self):
        """Fetch all weather-related data with caching."""
        # Check if cached data is available and not expired
        if "weather_data" in self.cache and (time.time() - self.cache["timestamp"]) < self.cache_timeout:
            print("Returning cached weather data")
            return self.cache["weather_data"]

        # Fetch new data
        lat, lng = await self.get_user_location()
        if not lat or not lng:
            return None

        air_quality = await self.get_air_quality(lat, lng)
        weather_data = await self.get_weather_data(lat, lng)

        if not weather_data:
            return None

        current = weather_data.get("current", {})
        weather_data = {
            "air_quality": air_quality,
            "temperature": current.get("temp", "N/A"),
            "humidity": current.get("humidity", "N/A"),
            "uv_index": current.get("uvi", "N/A"),
            "wind_speed": current.get("wind_speed", "N/A"),
        }

        # Update the cache
        self.cache["weather_data"] = weather_data
        self.cache["timestamp"] = time.time()
        print("Updated weather data cache")

        return weather_data