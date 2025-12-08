"""
API-based weather data fetcher using OpenWeatherMap and WeatherAPI.
Demonstrates: Inheritance, parameter overloading
"""
from typing import List, Optional, Union
from datetime import datetime, timedelta
import requests
from scrapers.base_scraper import BaseWeatherScraper, ScraperConfig


class APIWeatherFetcher(BaseWeatherScraper):
    """Fetches weather data from free weather APIs."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        config: Optional[ScraperConfig] = None
    ) -> None:
        super().__init__(config)
        self.api_key: Optional[str] = api_key
        self.base_url: str = "https://api.open-meteo.com/v1"
    
    def get_source_name(self) -> str:
        return "Open-Meteo API"
    
    # Parameter overloading through default arguments and Union types
    def fetch_current_weather(
        self, 
        location: Union[str, tuple], 
        include_forecast: bool = False
    ) -> dict:
        """
        Fetch current weather data.
        Args:
            location: City name or (latitude, longitude) tuple
            include_forecast: Whether to include forecast data
        """
        lat, lon = self._resolve_location(location)
        
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "temperature_unit": "celsius"
        }
        
        if include_forecast:
            params["hourly"] = "temperature_2m,relativehumidity_2m"
        
        try:
            response = requests.get(
                url, 
                params=params, 
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return self._parse_current_weather(data, location)
        
        except requests.RequestException as e:
            print(f"❌ Error fetching weather for {location}: {e}")
            return {}
    
    def fetch_historical_weather(
        self,
        location: Union[str, tuple],
        start_date: datetime,
        end_date: datetime
    ) -> List[dict]:
        """Fetch historical weather data for a date range."""
        lat, lon = self._resolve_location(location)
        
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }
        
        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return self._parse_historical_weather(data, location)
        
        except requests.RequestException as e:
            print(f"❌ Error fetching historical data for {location}: {e}")
            return []
    
    def _resolve_location(self, location: Union[str, tuple]) -> tuple:
        """
        Resolve location to (latitude, longitude).
        Demonstrates method overloading pattern.
        """
        if isinstance(location, tuple):
            return location
        
        # Simple geocoding for common cities
        city_coords = {
            "london": (51.5074, -0.1278),
            "new york": (40.7128, -74.0060),
            "tokyo": (35.6762, 139.6503),
            "paris": (48.8566, 2.3522),
            "istanbul": (41.0082, 28.9784),
            "berlin": (52.5200, 13.4050),
            "sydney": (-33.8688, 151.2093),
            "moscow": (55.7558, 37.6173)
        }
        
        location_lower = location.lower()
        return city_coords.get(location_lower, (51.5074, -0.1278))
    
    def _parse_current_weather(self, data: dict, location: Union[str, tuple]) -> dict:
        """Parse current weather response."""
        if "current_weather" not in data:
            return {}
        
        current = data["current_weather"]
        location_name = location if isinstance(location, str) else f"{location[0]:.2f},{location[1]:.2f}"
        
        return {
            "location": location_name,
            "temperature": current.get("temperature", 0.0),
            "windspeed": current.get("windspeed", 0.0),
            "winddirection": current.get("winddirection", 0),
            "weathercode": current.get("weathercode", 0),
            "timestamp": datetime.fromisoformat(current.get("time", datetime.now().isoformat())),
            "source": self.get_source_name()
        }
    
    def _parse_historical_weather(self, data: dict, location: Union[str, tuple]) -> List[dict]:
        """Parse historical weather response."""
        if "daily" not in data:
            return []
        
        daily = data["daily"]
        location_name = location if isinstance(location, str) else f"{location[0]:.2f},{location[1]:.2f}"
        
        records = []
        times = daily.get("time", [])
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        precipitation = daily.get("precipitation_sum", [])
        
        for i in range(len(times)):
            records.append({
                "location": location_name,
                "date": datetime.fromisoformat(times[i]),
                "temperature_max": temp_max[i] if i < len(temp_max) else None,
                "temperature_min": temp_min[i] if i < len(temp_min) else None,
                "precipitation": precipitation[i] if i < len(precipitation) else None,
                "source": self.get_source_name()
            })
        
        return records
