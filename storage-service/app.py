from fastapi import FastAPI
import uvicorn
from kafka import KafkaProducer
import json
import consumer

app = FastAPI(title="Storage Service")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.on_event("startup")
async def startup_event():
    consumer.run_consumer()

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