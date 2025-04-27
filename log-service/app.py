from fastapi import FastAPI
import uvicorn
from kafka import KafkaProducer
import json
app = FastAPI(title="User Service")

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