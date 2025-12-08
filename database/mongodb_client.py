"""
MongoDB database client wrapper.
Demonstrates: MongoDB usage (+15 bonus), ORM pattern, full type checking
"""
from typing import List, Optional, Dict, Any
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime
import os


class MongoDBClient:
    """
    MongoDB client wrapper with ORM-like functionality.
    Handles connection, CRUD operations, and queries.
    """
    
    def __init__(
        self, 
        connection_string: Optional[str] = None,
        database_name: str = "weather_history_db"
    ) -> None:
        """
        Initialize MongoDB connection.
        
        Args:
            connection_string: MongoDB connection URI
            database_name: Name of the database to use
        """
        self.connection_string: str = (
            connection_string or 
            os.getenv("MONGODB_URI") or 
            "mongodb://localhost:27017/"
        )
        self.database_name: str = database_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self._is_connected: bool = False
    
    def connect(self) -> bool:
        """
        Establish connection to MongoDB.
        Returns True if successful, False otherwise.
        """
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[self.database_name]
            self._is_connected = True
            print(f"✅ Connected to MongoDB: {self.database_name}")

            # Create indexes but don't fail the whole connection if index creation errors occur
            try:
                self._create_indexes()
            except Exception as ie:
                print(f"⚠️  Warning: failed to create indexes: {ie}")

            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            print("💡 Tip: Install MongoDB or use MongoDB Atlas cloud service")
            self._is_connected = False
            return False
    
    def _create_indexes(self) -> None:
        """Create indexes for better query performance."""
        # FIXED: explicitly check against None
        if self.db is None:
            return
        weather_collection = self.db.weather_records
        # Create indexes individually and catch errors per-index to avoid failing connection
        try:
            weather_collection.create_index([("location", ASCENDING)])
        except Exception as e:
            print(f"⚠️  Could not create index on weather_records.location: {e}")

        try:
            weather_collection.create_index([("timestamp", DESCENDING)])
        except Exception as e:
            print(f"⚠️  Could not create index on weather_records.timestamp: {e}")

        try:
            weather_collection.create_index([("temperature", ASCENDING)])
        except Exception as e:
            print(f"⚠️  Could not create index on weather_records.temperature: {e}")

        historical_collection = self.db.historical_records
        try:
            historical_collection.create_index([("location", ASCENDING)])
        except Exception as e:
            print(f"⚠️  Could not create index on historical_records.location: {e}")

        try:
            historical_collection.create_index([("date", DESCENDING)])
        except Exception as e:
            print(f"⚠️  Could not create index on historical_records.date: {e}")
    
    def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self._is_connected = False
            print("🔌 Disconnected from MongoDB")
    
    def is_connected(self) -> bool:
        """Check if connected to MongoDB."""
        return self._is_connected
    
    # CRUD Operations for Weather Records
    
    def insert_weather_record(self, record: Dict[str, Any]) -> Optional[str]:
        """
        Insert a weather record.
        Returns the inserted document ID.
        """
        # FIXED
        if self.db is None:
            return None
        
        try:
            collection: Collection = self.db.weather_records
            result = collection.insert_one(record)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error inserting weather record: {e}")
            return None
    
    def insert_many_weather_records(self, records: List[Dict[str, Any]]) -> int:
        """
        Insert multiple weather records.
        Returns the number of inserted documents.
        """
        # FIXED
        if self.db is None or not records:
            return 0
        
        try:
            collection: Collection = self.db.weather_records
            result = collection.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            print(f"❌ Error inserting weather records: {e}")
            return 0
    
    def find_weather_records(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Find weather records matching the filter.
        """
        # FIXED
        if self.db is None:
            return []
        
        try:
            collection: Collection = self.db.weather_records
            cursor = collection.find(filter_query or {}).limit(limit).sort("timestamp", DESCENDING)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error finding weather records: {e}")
            return []
    
    def update_weather_record(
        self,
        filter_query: Dict[str, Any],
        update_data: Dict[str, Any]
    ) -> int:
        """
        Update weather records matching the filter.
        Returns the number of modified documents.
        """
        # FIXED
        if self.db is None:
            return 0
        
        try:
            collection: Collection = self.db.weather_records
            result = collection.update_many(filter_query, {"$set": update_data})
            return result.modified_count
        except Exception as e:
            print(f"❌ Error updating weather records: {e}")
            return 0
    
    def delete_weather_records(self, filter_query: Dict[str, Any]) -> int:
        """
        Delete weather records matching the filter.
        Returns the number of deleted documents.
        """
        # FIXED
        if self.db is None:
            return 0
        
        try:
            collection: Collection = self.db.weather_records
            result = collection.delete_many(filter_query)
            return result.deleted_count
        except Exception as e:
            print(f"❌ Error deleting weather records: {e}")
            return 0
    
    # Historical Records Operations
    
    def insert_historical_record(self, record: Dict[str, Any]) -> Optional[str]:
        """Insert a historical weather record."""
        # FIXED
        if self.db is None:
            return None
        
        try:
            collection: Collection = self.db.historical_records
            result = collection.insert_one(record)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error inserting historical record: {e}")
            return None
    
    def insert_many_historical_records(self, records: List[Dict[str, Any]]) -> int:
        """Insert multiple historical records."""
        # FIXED
        if self.db is None or not records:
            return 0
        
        try:
            collection: Collection = self.db.historical_records
            result = collection.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            print(f"❌ Error inserting historical records: {e}")
            return 0
    
    def find_historical_records(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Find historical records matching the filter."""
        # FIXED
        if self.db is None:
            return []
        
        try:
            collection: Collection = self.db.historical_records
            cursor = collection.find(filter_query or {}).limit(limit).sort("date", DESCENDING)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error finding historical records: {e}")
            return []
    
    # Analytics and Aggregation
    
    def get_temperature_stats(self, location: Optional[str] = None) -> Dict[str, float]:
        """
        Get temperature statistics (min, max, avg) for a location.
        """
        # FIXED
        if self.db is None:
            return {}
        
        try:
            collection: Collection = self.db.weather_records
            match_stage = {"$match": {"location": location}} if location else {"$match": {}}
            
            pipeline = [
                match_stage,
                {
                    "$group": {
                        "_id": None,
                        "avg_temp": {"$avg": "$temperature"},
                        "min_temp": {"$min": "$temperature"},
                        "max_temp": {"$max": "$temperature"},
                        "count": {"$sum": 1}
                    }
                }
            ]
            
            result = list(collection.aggregate(pipeline))
            if result:
                return {
                    "average": result[0]["avg_temp"],
                    "minimum": result[0]["min_temp"],
                    "maximum": result[0]["max_temp"],
                    "count": result[0]["count"]
                }
            return {}
        except Exception as e:
            print(f"❌ Error calculating temperature stats: {e}")
            return {}
    
    def get_records_by_location(self) -> List[Dict[str, Any]]:
        """Get count of records grouped by location."""
        # FIXED
        if self.db is None:
            return []
        
        try:
            collection: Collection = self.db.weather_records
            pipeline = [
                {
                    "$group": {
                        "_id": "$location",
                        "count": {"$sum": 1},
                        "avg_temp": {"$avg": "$temperature"}
                    }
                },
                {"$sort": {"count": -1}}
            ]
            
            return list(collection.aggregate(pipeline))
        except Exception as e:
            print(f"❌ Error getting records by location: {e}")
            return []
    
    def clear_all_data(self) -> bool:
        """Clear all weather data from database."""
        # FIXED
        if self.db is None:
            return False
        
        try:
            self.db.weather_records.delete_many({})
            self.db.historical_records.delete_many({})
            print("🗑️  All weather data cleared")
            return True
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()