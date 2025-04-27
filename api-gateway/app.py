from fastapi import FastAPI
import httpx
import uvicorn

app = FastAPI(title="API Gateway")

# Service URLs
ORDER_SERVICE_URL = "http://order-service:8081"
STORAGE_SERVICE_URL = "http://storage-service:8082"
LOG_SERVICE_URL = "http://log-service:8083"

@app.get("/")
async def gateway_root():
    return {"message": "Welcome to E-commerce API Gateway"}

@app.get("/api/health")
async def check_services():
    async with httpx.AsyncClient() as client:
        try:
            users = await client.get(f"{ORDER_SERVICE_URL}/health")
            products = await client.get(f"{STORAGE_SERVICE_URL}/health")
            orders = await client.get(f"{LOG_SERVICE_URL}/health")
            
            return {
                "gateway": "healthy",
                "user_service": users.json(),
                "product_service": products.json(),
                "order_service": orders.json()
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) 