"""
Business logic for weather data analysis and filtering.
Demonstrates: OOP, inheritance, business logic layer
"""
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime, timedelta
from models.weather_models import WeatherRecord, HistoricalWeatherRecord, WeatherQuery
from abc import ABC, abstractmethod


class WeatherFilter(ABC):
    """
    Abstract base class for weather filters.
    Demonstrates: Strategy pattern for filtering.
    """
    
    @abstractmethod
    def apply(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply filter to weather records."""
        pass


class TemperatureRangeFilter(WeatherFilter):
    """Filter records by temperature range."""
    
    def __init__(self, min_temp: Optional[float] = None, max_temp: Optional[float] = None):
        self.min_temp = min_temp
        self.max_temp = max_temp
    
    def apply(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter records within temperature range."""
        filtered = records
        
        if self.min_temp is not None:
            filtered = [r for r in filtered if r.get('temperature', 0) >= self.min_temp]
        
        if self.max_temp is not None:
            filtered = [r for r in filtered if r.get('temperature', 0) <= self.max_temp]
        
        return filtered


class DateRangeFilter(WeatherFilter):
    """Filter records by date range."""
    
    def __init__(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        self.start_date = start_date
        self.end_date = end_date
    
    def apply(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter records within date range."""
        filtered = records
        
        for record in filtered[:]:
            timestamp_str = record.get('timestamp') or record.get('date')
            if not timestamp_str:
                continue
            
            if isinstance(timestamp_str, str):
                timestamp = datetime.fromisoformat(timestamp_str)
            else:
                timestamp = timestamp_str
            
            if self.start_date and timestamp < self.start_date:
                filtered.remove(record)
                continue
            
            if self.end_date and timestamp > self.end_date:
                if record in filtered:
                    filtered.remove(record)
        
        return filtered


class LocationFilter(WeatherFilter):
    """Filter records by location."""
    
    def __init__(self, location: str):
        self.location = location.lower()
    
    def apply(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter records matching location."""
        return [
            r for r in records 
            if self.location in r.get('location', '').lower()
        ]


class WeatherAnalyzer:
    """
    Analyze weather data and provide insights.
    Demonstrates: Business logic, data analysis.
    """
    
    def __init__(self):
        self.filters: List[WeatherFilter] = []
    
    def add_filter(self, filter_obj: WeatherFilter) -> 'WeatherAnalyzer':
        """Add a filter to the analyzer (builder pattern)."""
        self.filters.append(filter_obj)
        return self
    
    def clear_filters(self) -> None:
        """Clear all filters."""
        self.filters.clear()
    
    def apply_filters(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply all filters to records."""
        filtered = records
        for filter_obj in self.filters:
            filtered = filter_obj.apply(filtered)
        return filtered
    
    def find_hottest_day(self, records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find the day with highest temperature."""
        if not records:
            return None
        
        return max(records, key=lambda x: x.get('temperature', float('-inf')))
    
    def find_coldest_day(self, records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find the day with lowest temperature."""
        if not records:
            return None
        
        return min(records, key=lambda x: x.get('temperature', float('inf')))
    
    def calculate_average_temperature(self, records: List[Dict[str, Any]]) -> Optional[float]:
        """Calculate average temperature from records."""
        if not records:
            return None
        
        temps = [r.get('temperature') for r in records if r.get('temperature') is not None]
        return sum(temps) / len(temps) if temps else None
    
    def calculate_temperature_trend(self, records: List[Dict[str, Any]]) -> str:
        """
        Determine if temperature is trending up, down, or stable.
        """
        if len(records) < 2:
            return "Insufficient data"
        
        # Sort by timestamp
        sorted_records = sorted(
            records,
            key=lambda x: datetime.fromisoformat(
                x.get('timestamp') or x.get('date', datetime.now().isoformat())
            )
        )
        
        first_half = sorted_records[:len(sorted_records)//2]
        second_half = sorted_records[len(sorted_records)//2:]
        
        avg_first = self.calculate_average_temperature(first_half)
        avg_second = self.calculate_average_temperature(second_half)
        
        if avg_first is None or avg_second is None:
            return "Insufficient data"
        
        diff = avg_second - avg_first
        
        if abs(diff) < 1.0:
            return f"Stable (±{abs(diff):.1f}°C)"
        elif diff > 0:
            return f"Warming (+{diff:.1f}°C)"
        else:
            return f"Cooling ({diff:.1f}°C)"
    
    def group_by_location(self, records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group records by location."""
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        
        for record in records:
            location = record.get('location', 'Unknown')
            if location not in grouped:
                grouped[location] = []
            grouped[location].append(record)
        
        return grouped
    
    def get_summary_statistics(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics.
        """
        if not records:
            return {"error": "No records to analyze"}
        
        temps = [r.get('temperature') for r in records if r.get('temperature') is not None]
        
        if not temps:
            return {"error": "No temperature data available"}
        
        return {
            "total_records": len(records),
            "average_temperature": sum(temps) / len(temps),
            "min_temperature": min(temps),
            "max_temperature": max(temps),
            "temperature_range": max(temps) - min(temps),
            "unique_locations": len(set(r.get('location') for r in records)),
            "trend": self.calculate_temperature_trend(records)
        }
    
    def compare_locations(
        self,
        records: List[Dict[str, Any]],
        location1: str,
        location2: str
    ) -> Dict[str, Any]:
        """
        Compare weather between two locations.
        """
        grouped = self.group_by_location(records)
        
        loc1_records = [r for r in records if location1.lower() in r.get('location', '').lower()]
        loc2_records = [r for r in records if location2.lower() in r.get('location', '').lower()]
        
        if not loc1_records or not loc2_records:
            return {"error": "Insufficient data for comparison"}
        
        avg1 = self.calculate_average_temperature(loc1_records)
        avg2 = self.calculate_average_temperature(loc2_records)
        
        return {
            "location1": location1,
            "location1_avg_temp": avg1,
            "location1_records": len(loc1_records),
            "location2": location2,
            "location2_avg_temp": avg2,
            "location2_records": len(loc2_records),
            "temperature_difference": abs(avg1 - avg2) if avg1 and avg2 else None,
            "warmer_location": location1 if (avg1 or 0) > (avg2 or 0) else location2
        }


class WeatherReportGenerator:
    """
    Generate formatted reports from weather data.
    Demonstrates: Report generation, formatting.
    """
    
    def __init__(self, analyzer: WeatherAnalyzer):
        self.analyzer = analyzer
    
    def generate_summary_report(self, records: List[Dict[str, Any]]) -> str:
        """Generate a summary report of weather data."""
        stats = self.analyzer.get_summary_statistics(records)
        
        if "error" in stats:
            return f"❌ {stats['error']}"
        
        report = "\n" + "="*60 + "\n"
        report += "📊 WEATHER SUMMARY REPORT\n"
        report += "="*60 + "\n\n"
        report += f"📝 Total Records: {stats['total_records']}\n"
        report += f"📍 Unique Locations: {stats['unique_locations']}\n"
        report += f"🌡️  Average Temperature: {stats['average_temperature']:.1f}°C\n"
        report += f"🔥 Maximum Temperature: {stats['max_temperature']:.1f}°C\n"
        report += f"❄️  Minimum Temperature: {stats['min_temperature']:.1f}°C\n"
        report += f"📈 Temperature Range: {stats['temperature_range']:.1f}°C\n"
        report += f"📉 Trend: {stats['trend']}\n"
        report += "="*60 + "\n"
        
        return report
    
    def generate_location_report(
        self,
        records: List[Dict[str, Any]],
        location: str
    ) -> str:
        """Generate a report for a specific location."""
        location_records = [
            r for r in records 
            if location.lower() in r.get('location', '').lower()
        ]
        
        if not location_records:
            return f"❌ No data found for location: {location}"
        
        stats = self.analyzer.get_summary_statistics(location_records)
        
        report = "\n" + "="*60 + "\n"
        report += f"📍 WEATHER REPORT FOR: {location.upper()}\n"
        report += "="*60 + "\n\n"
        report += f"📝 Total Records: {stats['total_records']}\n"
        report += f"🌡️  Average Temperature: {stats['average_temperature']:.1f}°C\n"
        report += f"🔥 Maximum Temperature: {stats['max_temperature']:.1f}°C\n"
        report += f"❄️  Minimum Temperature: {stats['min_temperature']:.1f}°C\n"
        report += f"📈 Trend: {stats['trend']}\n"
        report += "="*60 + "\n"
        
        return report
