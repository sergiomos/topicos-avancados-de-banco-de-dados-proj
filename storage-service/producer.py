from kafka import KafkaProducer
import json
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Inicializa o produtor Kafka
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Produtor Kafka inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar o produtor Kafka: {str(e)}")
    producer = None

def send_storage_response(event_type: str, success: bool, data: dict = None):
    """
    Envia uma mensagem de resposta para o tópico storage-response
    
    Args:
        event_type (str): Tipo do evento processado
        success (bool): Indica se o processamento foi bem-sucedido
        data (dict, optional): Dados processados ou informações de erro
    """
    try:
        if producer:
            message = {
                'event_type': event_type,
                'success': success,
                'data': data
            }
            
            future = producer.send('storage-response', message)
            # Aguarda o envio da mensagem
            result = future.get(timeout=60)
            logger.info(f"Resposta de armazenamento enviada com sucesso. Tópico: {result.topic}, Partição: {result.partition}, Offset: {result.offset}")
        else:
            logger.error("Produtor não inicializado")
    except Exception as e:
        logger.error(f"Erro ao enviar resposta de armazenamento: {str(e)}") 