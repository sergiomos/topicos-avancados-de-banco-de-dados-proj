from fastapi import FastAPI
import uvicorn
from kafka import KafkaProducer
import json
import controllers.usuario as usuario
app = FastAPI(title="Order Service")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.get("/")
async def root():
    return {"message": "Order Service - Hello World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "order-service"}

@app.post("/api/popular/clientes")
async def get_clientes():
    return usuario.gerar_clientes(10)

@app.post("/api/popular/vendedores")
async def get_vendedores():
    return usuario.gerar_vendedores(10)


@app.post("/api/orders/event")
async def create_order_event(event_type: str, order_id: str):
    # Example of Kafka message publishing
    producer.send('order-events', {
        'event_type': event_type,
        'order_id': order_id
    })
    return {"message": "Event published successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081) 