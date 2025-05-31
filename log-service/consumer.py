from kafka import KafkaConsumer
import json
import logging
import threading
from datetime import datetime

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_storage_response(event_data):
    """
    Processa eventos de resposta do serviço de armazenamento
    
    Args:
        event_data (dict): Dados do evento recebido
    """
    try:
        event_type = event_data.get('event_type')
        success = event_data.get('success')
        data = event_data.get('data', {})
        
        # Cria mensagem de log
        log_message = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'success': success,
            'data': data,
            'source_service': 'storage-service'
        }
        
        # Log baseado no sucesso da operação
        if success:
            logger.info(f"Evento de armazenamento processado com sucesso: {event_type}")
            logger.debug(f"Detalhes do evento: {json.dumps(log_message, indent=2)}")
        else:
            logger.error(f"Falha no processamento do evento de armazenamento: {event_type}")
            logger.error(f"Detalhes do erro: {json.dumps(log_message, indent=2)}")
            
    except Exception as e:
        logger.error(f"Erro ao processar evento de resposta de armazenamento: {str(e)}")

def start_consumer():
    """
    Inicia o consumidor Kafka para o tópico storage-response
    """
    try:
        # Cria consumidor para o tópico storage-response
        consumer = KafkaConsumer(
            'storage-response',
            bootstrap_servers=['kafka:9092'],
            group_id='log-service-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        logger.info("Consumidor Kafka iniciado com sucesso")
        
        # Processa mensagens
        for message in consumer:
            try:
                event_data = message.value
                handle_storage_response(event_data)
            except Exception as e:
                logger.error(f"Erro ao processar mensagem: {str(e)}")
            
    except Exception as e:
        logger.error(f"Erro no consumidor: {str(e)}")

def run_consumer():
    """
    Inicia o consumidor em uma thread separada
    """
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start() 