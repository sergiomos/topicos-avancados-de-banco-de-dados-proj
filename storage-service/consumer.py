from kafka import KafkaConsumer
import json
import logging
import threading
from controllers.cliente_controller import ClienteController
from controllers.vendedor_controller import VendedorController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_user_event(event_data):
    event_type = event_data.get('event_type')
    if event_type == 'novo_cliente':
        cliente_data = event_data.get('data', {})
        success = ClienteController.insert_cliente(cliente_data)
    elif event_type == 'novo_vendedor': 
        vendedor_data = event_data.get('data', {})
        success = VendedorController.insert_vendedor(vendedor_data)
    else:
        logger.info(f"Received message with event-type: {event_type}")
    if not success:
        logger.error(f"Failed to process user event for {event_type}")

def start_consumer():
    try:
        consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers=['kafka:9092'],
            group_id='test-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        logger.info("Kafka Consumer started successfully")
        
        for message in consumer:
            try:
                event_data = message.value
                handle_user_event(event_data)
                    
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error in consumer: {str(e)}")

def run_consumer():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start() 