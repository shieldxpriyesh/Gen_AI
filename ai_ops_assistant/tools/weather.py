import requests
from typing import Dict, Any
from .base import BaseTool

class WeatherTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a specific city."
        )

    def execute(self, city: str, **kwargs) -> Dict[str, Any]:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_response = requests.get(geo_url).json()
            
            if not geo_response.get("results"):
                return {"error": f"City '{city}' not found."}
            
            location = geo_response["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url).json()
            
            current_weather = weather_response.get("current_weather", {})
            return {
                "city": location["name"],
                "temperature": current_weather.get("temperature"),
                "windspeed": current_weather.get("windspeed"),
                "weathercode": current_weather.get("weathercode")
            }
        except Exception as e:
            return {"error": str(e)}

    def to_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city to get weather for"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
