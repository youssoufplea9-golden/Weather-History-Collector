"""
Abstract base class for all weather data scrapers.
Demonstrates: Abstract classes, protocols, full type checking
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from dataclasses import dataclass
from datetime import datetime


class WeatherDataProtocol(Protocol):
    """Protocol defining the interface for weather data."""
    location: str
    temperature: float
    humidity: float
    timestamp: datetime


@dataclass
class ScraperConfig:
    """Configuration for scrapers with full type hints."""
    timeout: int = 30
    max_retries: int = 3
    user_agent: str = "WeatherCollector/1.0"


class BaseWeatherScraper(ABC):
    """
    Abstract base class for all weather scrapers.
    Implements template method pattern.
    """
    
    def __init__(self, config: Optional[ScraperConfig] = None) -> None:
        self.config: ScraperConfig = config or ScraperConfig()
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate scraper configuration."""
        if self.config.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.config.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
    
    @abstractmethod
    def fetch_current_weather(self, location: str) -> dict:
        """
        Fetch current weather data for a location.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def fetch_historical_weather(
        self, 
        location: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[dict]:
        """
        Fetch historical weather data for a date range.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the data source."""
        pass
    
    def preprocess_data(self, raw_data: dict) -> dict:
        """
        Preprocess raw data before storage.
        Can be overridden by subclasses.
        """
        return raw_data
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(source={self.get_source_name()})"
