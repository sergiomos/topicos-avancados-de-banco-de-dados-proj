from fastapi import FastAPI
import uvicorn
from kafka import KafkaProducer
import json

app = FastAPI(
    title="Log Service",
    description="""
    Service responsible for logging all system events.
    
    ## Kafka Integration
    This service consumes events from the following topics:
    
    ### Topic: user-events
    - **novo_cliente**: Logs new client registrations
    - **novo_vendedor**: Logs new seller registrations
    
    ### Event Processing:
    All events are logged with the following information:
    - Timestamp
    - Event type
    - Event data
    - Source service
    """
)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.get("/")
async def root():
    return {"message": "Log Service - Hello World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "log-service"}

@app.post("/api/log/event")
async def create_user_event(event_type: str, user_id: str):
    # Example of Kafka message publishing
    producer.send('user-events', {
        'event_type': event_type,
        'user_id': user_id
    })
    return {"message": "Event published successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083) 