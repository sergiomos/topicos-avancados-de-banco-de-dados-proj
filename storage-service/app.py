from fastapi import FastAPI, HTTPException
import uvicorn
import logging
from database.postgres import PostgresConnection
from database.mongodb import MongoDBConnection
from database.cassandra import CassandraConnection
from database.init_db import init_database
import consumer
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController
from controllers.pedido_controller import PedidoController
#from database import PostgresConnection, MongoDBConnection, CassandraConnection

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Serviço de Armazenamento",
    description="Serviço responsável por armazenar dados em diferentes bancos de dados",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Inicializa conexões com bancos de dados e tabelas quando a aplicação inicia"""
    try:
        # Inicializa conexão com PostgreSQL
        PostgresConnection.initialize()
        
        # Inicializa tabelas do banco de dados
        if not init_database():
            raise Exception("Falha ao inicializar tabelas do banco de dados")
        
        # Inicializa conexão com MongoDB
        MongoDBConnection.initialize()
        
        # Inicializa conexão com Cassandra
        CassandraConnection.initialize()

        # Inicia consumidor Kafka
        consumer.run_consumer()
        
        logger.info("Todas as conexões com bancos de dados e tabelas inicializadas com sucesso")
    except Exception as e:
        logger.error(f"Erro durante a inicialização: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Fecha conexões com bancos de dados quando a aplicação é encerrada"""
    try:
        # Fecha conexões PostgreSQL
        PostgresConnection.close_all()
        
        # Fecha conexão MongoDB
        MongoDBConnection.close()
        
        # Fecha conexão Cassandra
        CassandraConnection.close()
        
        logger.info("Todas as conexões com bancos de dados fechadas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao fechar conexões com bancos de dados: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Serviço de Armazenamento - Olá Mundo!"}

@app.get("/health")
async def health_check():
    return {"status": "saudável", "service": "Serviço de Armazenamento"}

@app.post("/api/storages/event")
async def create_storage_event(event_type: str, storage_id: str):
    # Exemplo de publicação de mensagem Kafka
    producer.send('storage-events', {
        'event_type': event_type,
        'storage_id': storage_id
    })
    return {"message": "Evento publicado com sucesso"}

@app.get("/api/clientes/{cliente_id}")
async def get_cliente(cliente_id: str):
    """
    Obtém um cliente pelo seu ID
    """
    cliente = ClienteController.get_cliente_by_id(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.get("/api/produtos/{produto_id}")
async def get_produto(produto_id: str):
    """
    Obtém um produto pelo seu ID
    """
    produto = ProdutoController.get_produto_by_id(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.get("/api/pedidos/{pedido_id}")
async def get_pedido(pedido_id: str):
    """
    Obtém um pedido pelo seu ID
    """
    pedido = PedidoController.get_pedido_by_id(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082) 
