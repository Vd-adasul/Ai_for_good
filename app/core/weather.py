import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherService:
    def get_weather(self, city: str):
        if not API_KEY:
            return None
        
        try:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temp": data["main"]["temp"],
                    "weather": data["weather"][0]["description"],
                    "city": data["name"]
                }
            return None
        except Exception:
            return None

weather_service = WeatherService()
