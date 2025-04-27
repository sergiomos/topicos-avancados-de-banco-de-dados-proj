from fastapi import FastAPI, Query
import uvicorn
import controllers.usuario as usuario
import producer

app = FastAPI(
    title="Gerar dados",
    description="Serviço responsável por gerar os dados do ecommerce",
    version="1.0.0",
    docs_url="/docs"
)

@app.get("/",
    summary="Root endpoint",
    description="Retorna uma mensagem de Hello World"
)
async def root():
    return {"message": "Gerar dados - Hello World!"}


@app.post("/api/popular/clientes",
    summary="Gerar uma quantidade de clientes",
    description="Gera uma quantidade de clientes para teste",
    response_description="Lista de dados de clientes gerados"
)
async def post_clientes(
    amount: int = Query(
        default=10,
        description="Quantidade de clientes a gerar",
        ge=1,
        le=100
    )
):
    clientes = usuario.gerar_clientes(amount)
    for cliente in clientes:
        producer.novo_cliente(cliente)
        
    return {"message": "Clientes gerados com sucesso",
            "data": clientes}

@app.post("/api/popular/vendedores",
    summary="Gerar uma quantidade de vendedores",
    description="Gera uma quantidade de vendedores para teste",
    response_description="Lista de dados de vendedores gerados"
)
async def get_vendedores(
    amount: int = Query(
        default=10,
        description="Quantidade de vendedores a gerar",
        ge=1,
        le=100
    )
):
    return usuario.gerar_vendedores(amount)

@app.post("/api/orders/event",
    summary="Create order event",
    description="Creates and publishes an order-related event to Kafka",
    response_description="Confirmation of event publication"
)
async def create_order_event(
    event_type: str = Query(..., description="Type of the order event"),
    order_id: str = Query(..., description="ID of the order")
):
    producer.order_event(event_type, order_id)
    return {"message": "Event published successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081) 