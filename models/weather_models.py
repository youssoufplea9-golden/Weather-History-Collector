"""
Weather data models using dataclasses and full type checking.
Demonstrates: Dataclasses, full type hints, validation
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class WeatherCondition(Enum):
    """Enumeration for weather conditions."""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    SNOWY = "snowy"
    STORMY = "stormy"
    FOGGY = "foggy"
    UNKNOWN = "unknown"


@dataclass(frozen=False)
class WeatherRecord:
    """
    Immutable weather record with full type hints.
    Demonstrates: Dataclass with validation and type checking.
    """
    location: str
    temperature: float
    timestamp: datetime
    source: str
    humidity: Optional[float] = None
    windspeed: Optional[float] = None
    precipitation: Optional[float] = None
    condition: Optional[str] = None
    record_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if self.temperature < -100 or self.temperature > 60:
            raise ValueError(f"Invalid temperature: {self.temperature}")
        
        if self.humidity is not None:
            if self.humidity < 0 or self.humidity > 100:
                raise ValueError(f"Invalid humidity: {self.humidity}")
        
        if self.windspeed is not None and self.windspeed < 0:
            raise ValueError(f"Invalid windspeed: {self.windspeed}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        data = asdict(self)
        # Convert datetime to ISO format string
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WeatherRecord':
        """Create WeatherRecord from dictionary."""
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
    
    def celsius_to_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit."""
        return (self.temperature * 9/5) + 32
    
    def __str__(self) -> str:
        return (
            f"📍 {self.location} | "
            f"🌡️  {self.temperature:.1f}°C | "
            f"💧 {self.humidity or 'N/A'}% | "
            f"⏰ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )


@dataclass
class HistoricalWeatherRecord:
    """
    Historical weather record for daily data.
    """
    location: str
    date: datetime
    temperature_max: Optional[float]
    temperature_min: Optional[float]
    precipitation: Optional[float]
    source: str
    record_id: Optional[str] = None
    condition: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate historical data."""
        if self.temperature_max is not None and self.temperature_min is not None:
            if self.temperature_max < self.temperature_min:
                raise ValueError(
                    f"Max temp ({self.temperature_max}) < Min temp ({self.temperature_min})"
                )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HistoricalWeatherRecord':
        """Create from dictionary."""
        if isinstance(data['date'], str):
            data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)
    
    def get_average_temp(self) -> Optional[float]:
        """Calculate average temperature."""
        if self.temperature_max is not None and self.temperature_min is not None:
            return (self.temperature_max + self.temperature_min) / 2
        return None
    
    def __str__(self) -> str:
        avg = self.get_average_temp()
        return (
            f"📍 {self.location} | "
            f"📅 {self.date.strftime('%Y-%m-%d')} | "
            f"🌡️  Max: {self.temperature_max:.1f}°C, Min: {self.temperature_min:.1f}°C "
            f"(Avg: {avg:.1f}°C) | "
            f"🌧️  {self.precipitation or 0:.1f}mm"
        )


@dataclass
class WeatherQuery:
    """
    Query parameters for weather searches.
    """
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    source: Optional[str] = None
    
    def to_mongo_filter(self) -> Dict[str, Any]:
        """Convert to MongoDB filter query."""
        filter_query: Dict[str, Any] = {}
        
        if self.location:
            filter_query['location'] = {"$regex": self.location, "$options": "i"}
        
        if self.start_date or self.end_date:
            date_filter: Dict[str, Any] = {}
            if self.start_date:
                date_filter['$gte'] = self.start_date.isoformat()
            if self.end_date:
                date_filter['$lte'] = self.end_date.isoformat()
            filter_query['timestamp'] = date_filter
        
        if self.min_temperature is not None or self.max_temperature is not None:
            temp_filter: Dict[str, Any] = {}
            if self.min_temperature is not None:
                temp_filter['$gte'] = self.min_temperature
            if self.max_temperature is not None:
                temp_filter['$lte'] = self.max_temperature
            filter_query['temperature'] = temp_filter
        
        if self.source:
            filter_query['source'] = self.source
        
        return filter_query
