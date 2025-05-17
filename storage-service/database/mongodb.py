from pymongo import MongoClient
import logging
from ..config import MONGODB_CONFIG

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _client = None
    _db = None

    @classmethod
    def initialize(cls):
        """Initialize the MongoDB connection"""
        try:
            cls._client = MongoClient(MONGODB_CONFIG['uri'])
            cls._db = cls._client.get_database()
            logger.info("MongoDB connection initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing MongoDB connection: {str(e)}")
            raise

    @classmethod
    def get_database(cls):
        """Get the database instance"""
        if cls._db is None:
            cls.initialize()
        return cls._db

    @classmethod
    def get_collection(cls, collection_name):
        """Get a collection from the database"""
        return cls.get_database()[collection_name]

    @classmethod
    def close(cls):
        """Close the MongoDB connection"""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")

    @classmethod
    def insert_one(cls, collection_name, document):
        """Insert a single document into a collection"""
        try:
            collection = cls.get_collection(collection_name)
            result = collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting document into MongoDB: {str(e)}")
            raise

    @classmethod
    def find_one(cls, collection_name, query):
        """Find a single document in a collection"""
        try:
            collection = cls.get_collection(collection_name)
            return collection.find_one(query)
        except Exception as e:
            logger.error(f"Error finding document in MongoDB: {str(e)}")
            raise 
