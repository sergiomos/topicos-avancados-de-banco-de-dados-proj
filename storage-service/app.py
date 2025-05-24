from fastapi import FastAPI
import uvicorn
import logging
from database.postgres import PostgresConnection
from database.mongodb import MongoDBConnection
from database.cassandra import CassandraConnection
from database.init_db import init_database
import consumer
#from database import PostgresConnection, MongoDBConnection, CassandraConnection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Storage Service",
    description="Service responsible for storing data in different databases",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database connections and tables when the application starts"""
    try:
        # Initialize PostgreSQL connection
        PostgresConnection.initialize()
        
        # Initialize database tables
        if not init_database():
            raise Exception("Failed to initialize database tables")
        
        # Initialize MongoDB connection
        MongoDBConnection.initialize()
        
        # Initialize Cassandra connection
        CassandraConnection.initialize()

        # Start Kafka consumer
        consumer.run_consumer()
        
        logger.info("All database connections and tables initialized successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections when the application shuts down"""
    try:
        # Close PostgreSQL connections
        PostgresConnection.close_all()
        
        # Close MongoDB connection
        MongoDBConnection.close()
        
        # Close Cassandra connection
        CassandraConnection.close()
        
        logger.info("All database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connections: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Storage Service - Hello World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Storage-service"}

@app.post("/api/storages/event")
async def create_storage_event(event_type: str, storage_id: str):
    # Example of Kafka message publishing
    producer.send('storage-events', {
        'event_type': event_type,
        'storage_id': storage_id
    })
    return {"message": "Event published successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082) 
