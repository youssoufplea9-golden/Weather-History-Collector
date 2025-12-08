# 🌤️ Weather History Collector

A comprehensive Python application for collecting, storing, and analyzing historical weather data. Built as a university project demonstrating advanced software engineering concepts.

## 🎯 Project Overview

Weather History Collector is a console-based application that fetches weather data from multiple sources, stores it in MongoDB, and provides powerful analysis tools.

## ✨ Features

- **Real-time Weather Data**: Fetch current weather from multiple locations
- **Historical Data Collection**: Retrieve weather history for date ranges
- **Advanced Search**: Filter records by location, temperature, and date
- **Statistical Analysis**: Generate comprehensive weather reports
- **Location Comparison**: Compare weather patterns between cities
- **Data Persistence**: MongoDB database for reliable storage

## 🏆 Bonus Points Achieved (40/45)

### Web Scraping & APIs (+10)
- ✅ Standard API usage (Open-Meteo API)
- ✅ **Scrapy framework** for advanced scraping (+10 bonus)

### Database (+15)
- ✅ **MongoDB** with full CRUD operations (+15 bonus)
- ✅ Indexing and aggregation pipelines
- ✅ Connection pooling and error handling

### Business Logic & OOP (+15)
- ✅ Abstract base classes and protocols
- ✅ **Dataclasses with full type checking** (+15 bonus)
- ✅ Inheritance and method overloading
- ✅ ORM-like database wrapper
- ✅ Strategy pattern for filtering
- ✅ Complete type hints throughout

## 📁 Project Structure

```
weather_history_collector/
│
├── scrapers/
│   ├── base_scraper.py          # Abstract base class with protocols
│   ├── api_weather_fetcher.py   # API implementation with inheritance
│   └── scrapy_weather_scraper.py # Scrapy-based scraper
│
├── database/
│   └── mongodb_client.py        # MongoDB ORM wrapper
│
├── models/
│   └── weather_models.py        # Dataclasses with full type checking
│
├── business_logic/
│   └── weather_analyzer.py      # Analysis and reporting logic
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/youssoufplea9-golden/Weather-History-Collector
cd Weather-History-Collector
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Setup MongoDB

**Option A: Local MongoDB**
```bash
# Install MongoDB Community Edition
# Start MongoDB service
mongod --dbpath /path/to/data/directory
```

**Option B: MongoDB Atlas (Cloud)**
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get your connection string
4. Set environment variable:
```bash
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
```

### Step 4: Run the Application

```bash
python main.py
```

## 📖 Usage Guide

### Main Menu Options

1. **Fetch Current Weather**: Get real-time weather for any city
2. **Fetch Historical Weather**: Retrieve weather data for past dates
3. **Search Weather Records**: Filter records by various criteria
4. **Generate Weather Report**: Create analysis reports
5. **View Statistics**: See temperature trends and statistics
6. **Compare Locations**: Compare weather between cities
7. **Clear All Data**: Reset the database
8. **View All Records**: Display stored weather data
9. **Exit**: Close the application

### Example Usage

#### Fetching Current Weather
```
Enter location: London
✅ Weather data fetched successfully!
📍 London | 🌡️ 15.0°C | 💧 N/A% | ⏰ 2025-12-08 13:30
```

#### Searching Records
```
Search filters:
Location: London
Minimum temperature (°C): 10
Maximum temperature (°C): 20

✅ Found 15 records matching your criteria
```

#### Generating Reports
```
📊 WEATHER SUMMARY REPORT
═══════════════════════════════════════
📝 Total Records: 150
📍 Unique Locations: 5
🌡️ Average Temperature: 15.3°C
🔥 Maximum Temperature: 28.5°C
❄️ Minimum Temperature: 2.1°C
📈 Temperature Range: 26.4°C
📉 Trend: Warming (+2.3°C)
```

## 🛠️ Technical Implementation

### Abstract Base Classes & Protocols

```python
class BaseWeatherScraper(ABC):
    @abstractmethod
    def fetch_current_weather(self, location: str) -> dict:
        pass
```

### Dataclasses with Type Checking

```python
@dataclass(frozen=False)
class WeatherRecord:
    location: str
    temperature: float
    timestamp: datetime
    source: str
    humidity: Optional[float] = None
```

### MongoDB ORM Pattern

```python
class MongoDBClient:
    def insert_weather_record(self, record: Dict[str, Any]) -> Optional[str]:
        collection = self.db.weather_records
        result = collection.insert_one(record)
        return str(result.inserted_id)
```

### Strategy Pattern for Filtering

```python
class TemperatureRangeFilter(WeatherFilter):
    def apply(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [r for r in records if self.min_temp <= r['temperature'] <= self.max_temp]
```

## 🧪 Type Checking

Run mypy for type checking:

```bash
mypy main.py scrapers/ database/ models/ business_logic/
```

## 📊 Database Schema

### Weather Records Collection
```json
{
  "_id": "ObjectId",
  "location": "string",
  "temperature": "float",
  "timestamp": "ISODate",
  "source": "string",
  "humidity": "float (optional)",
  "windspeed": "float (optional)"
}
```

### Historical Records Collection
```json
{
  "_id": "ObjectId",
  "location": "string",
  "date": "ISODate",
  "temperature_max": "float",
  "temperature_min": "float",
  "precipitation": "float",
  "source": "string"
}
```

## 🎓 Educational Concepts Demonstrated

1. **Object-Oriented Programming**
   - Inheritance and polymorphism
   - Abstract base classes
   - Protocol classes
   - Encapsulation

2. **Design Patterns**
   - Strategy Pattern (filters)
   - Template Method Pattern (base scraper)
   - Builder Pattern (analyzer)
   - Singleton Pattern (database client)

3. **Type Safety**
   - Full type hints
   - Dataclasses
   - Generic types
   - Optional types

4. **Database Design**
   - NoSQL schema design
   - Indexing strategies
   - Aggregation pipelines
   - CRUD operations

5. **Error Handling**
   - Try-except blocks
   - Validation
   - Graceful degradation

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=weather_history_db
API_TIMEOUT=30
```

## 📝 Development Notes

- The application uses **Open-Meteo API** (no API key required)
- Scrapy implementation is simplified for console-based usage
- MongoDB connection falls back to offline mode if unavailable
- Type checking enforced with mypy
- Full documentation in docstrings

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
mongod --version

# Test connection
mongo --eval "db.runCommand({ ping: 1 })"
```

### Module Import Errors

```bash
# Ensure you're in the correct directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Type Checking Errors

```bash
# Install type stubs
pip install types-requests types-pymongo
```

## 📚 Dependencies

- **requests**: HTTP API calls
- **scrapy**: Advanced web scraping
- **pymongo**: MongoDB driver
- **pydantic**: Data validation
- **mypy**: Static type checking

## 👥 Contributing

This is a university project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- Open-Meteo for free weather API
- MongoDB for database platform
- Python community for excellent libraries

## 📞 Contact

For questions or feedback about this project, please open an issue on GitHub.

---

**Built with ❤️ for Software Engineering Course**

**Bonus Points Target: 40/45** ✅
- Scrapy: +10 ✅
- MongoDB: +15 ✅
- Advanced OOP: +15 ✅
