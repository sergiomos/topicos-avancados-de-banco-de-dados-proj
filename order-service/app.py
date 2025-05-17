from fastapi import FastAPI, Query
import uvicorn
import controllers.usuario as usuario
import controllers.produto as produto
import controllers.pedido as pedido
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
    vendedores = usuario.gerar_vendedores(amount)
    for vendedor in vendedores:
        producer.novo_vendedor(vendedor)

    return {"message": "Vendedores gerados com sucesso",
            "data": vendedores}

@app.post("/api/popular/produtos",
    summary="Gerar uma quantidade de produtos",
    description="Gera uma quantidade de produtos para teste",
    response_description="Lista de dados de produtos gerados"
)
async def post_produtos(
    amount: int = Query(
        default=10,
        description="Quantidade de produtos a gerar",
        ge=1,
        le=100
    )
):
    produtos = produto.gerar_produtos(amount)
    for produto in produtos:
        producer.novo_produto(produto)

    return {"message": "Produtos gerados com sucesso",
            "data": produtos}

@app.post("/api/popular/pedidos",
    summary="Gerar uma quantidade de pedidos",
    description="Gera uma quantidade de pedidos para teste",
    response_description="Lista de dados de pedidos gerados"
)
async def post_pedidos(
    amount: int = Query(
        default=10,
        description="Quantidade de pedidos a gerar",
        ge=1,
        le=100
    ),
    qtd_clientes: int = Query(
        default=10,
        description="Quantidade de clientes para referência",
        ge=1,
        le=100
    ),
    qtd_vendedores: int = Query(
        default=5,
        description="Quantidade de vendedores para referência",
        ge=1,
        le=100
    ),
    qtd_produtos: int = Query(
        default=15,
        description="Quantidade de produtos para referência",
        ge=1,
        le=100
    )
):
    dados = pedido.gerar_dados(qtd_clientes, qtd_vendedores, qtd_produtos, amount)
    for pedido in dados['pedidos']:
        producer.novo_pedido(pedido)

    return {"message": "Pedidos gerados com sucesso",
            "data": dados['pedidos']}

@app.post("/api/popular/todos",
    summary="Gerar todas as entidades juntas",
    description="Gera clientes, vendedores, produtos e pedidos em uma única chamada",
    response_description="Dados gerados para todas as entidades"
)
async def post_todos(
    qtd_clientes: int = Query(
        default=10,
        description="Quantidade de clientes a gerar",
        ge=1,
        le=100
    ),
    qtd_vendedores: int = Query(
        default=5,
        description="Quantidade de vendedores a gerar",
        ge=1,
        le=100
    ),
    qtd_produtos: int = Query(
        default=15,
        description="Quantidade de produtos a gerar",
        ge=1,
        le=100
    ),
    qtd_pedidos: int = Query(
        default=20,
        description="Quantidade de pedidos a gerar",
        ge=1,
        le=100
    )
):
    dados = pedido.gerar_dados(qtd_clientes, qtd_vendedores, qtd_produtos, qtd_pedidos)
    
    # Enviar todos os dados para o Kafka
    for cliente in dados['clientes']:
        producer.novo_cliente(cliente)
    
    for vendedor in dados['vendedores']:
        producer.novo_vendedor(vendedor)
    
    for produto in dados['produtos']:
        producer.novo_produto(produto)
    
    for pedido in dados['pedidos']:
        producer.novo_pedido(pedido)

    return {"message": "Todos os dados foram gerados com sucesso",
            "data": dados}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081) 
