from fastapi import FastAPI
import uvicorn
from kafka import KafkaProducer
import json
import logging
import consumer

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Serviço de Log",
    description="""
    Serviço responsável por registrar todos os eventos do sistema.
    
    ## Integração com Kafka
    Este serviço consome eventos dos seguintes tópicos:
    
    ### Tópico: storage-response
    - **novo_cliente**: Registra novas inserções/atualizações de clientes
    - **novo_vendedor**: Registra novas inserções/atualizações de vendedores
    - **novo_produto**: Registra novas inserções/atualizações de produtos
    - **novo_pedido**: Registra novas inserções/atualizações de pedidos
    
    ### Processamento de Eventos:
    Todos os eventos são registrados com as seguintes informações:
    - Timestamp
    - Tipo do evento
    - Dados do evento
    - Serviço de origem
    - Status de sucesso/falha
    """
)

# Inicializa o produtor Kafka
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.on_event("startup")
async def startup_event():
    """Inicializa o consumidor Kafka quando a aplicação inicia"""
    try:
        consumer.run_consumer()
        logger.info("Consumidor Kafka iniciado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao iniciar consumidor Kafka: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "Serviço de Log - Olá Mundo!"}

@app.get("/health")
async def health_check():
    return {"status": "saudável", "service": "serviço-de-log"}

@app.post("/api/log/event")
async def create_user_event(event_type: str, user_id: str):
    # Exemplo de publicação de mensagem Kafka
    producer.send('user-events', {
        'event_type': event_type,
        'user_id': user_id
    })
    return {"message": "Evento publicado com sucesso"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083) 