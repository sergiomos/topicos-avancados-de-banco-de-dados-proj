from kafka import KafkaConsumer
import json
import logging
import threading
from controllers.cliente_controller import ClienteController
from controllers.vendedor_controller import VendedorController
from controllers.produto_controller import ProdutoController
from controllers.pedido_controller import PedidoController

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

def handle_product_event(event_data):
    event_type = event_data.get('event_type')
    if event_type == 'novo_produto':
        produto_data = event_data.get('data', {})
        success = ProdutoController.insert_produto(produto_data)
        if not success:
            logger.error(f"Failed to process product event for {event_type}")
    else:
        logger.info(f"Received message with event-type: {event_type}")

def handle_order_event(event_data):
    event_type = event_data.get('event_type')
    if event_type == 'novo_pedido':
        pedido_data = event_data.get('data', {})
        success = PedidoController.insert_pedido(pedido_data)
        if not success:
            logger.error(f"Failed to process order event for {event_type}")
    else:
        logger.info(f"Received message with event-type: {event_type}")

def start_consumer():
    try:
        # Create consumers for each topic
        user_consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers=['kafka:9092'],
            group_id='storage-service-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        product_consumer = KafkaConsumer(
            'product-events',
            bootstrap_servers=['kafka:9092'],
            group_id='storage-service-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        order_consumer = KafkaConsumer(
            'order-events',
            bootstrap_servers=['kafka:9092'],
            group_id='storage-service-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        logger.info("Kafka Consumers started successfully")
        
        # Process messages from all consumers
        while True:
            # Process user events
            for message in user_consumer:
                try:
                    event_data = message.value
                    handle_user_event(event_data)
                except Exception as e:
                    logger.error(f"Error processing user message: {str(e)}")
            
            # Process product events
            for message in product_consumer:
                try:
                    event_data = message.value
                    handle_product_event(event_data)
                except Exception as e:
                    logger.error(f"Error processing product message: {str(e)}")
            
            # Process order events
            for message in order_consumer:
                try:
                    event_data = message.value
                    handle_order_event(event_data)
                except Exception as e:
                    logger.error(f"Error processing order message: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error in consumer: {str(e)}")

def run_consumer():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start() 