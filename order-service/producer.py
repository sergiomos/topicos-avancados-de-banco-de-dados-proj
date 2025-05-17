from kafka import KafkaProducer
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Kafka Producer successfully initialized")
except Exception as e:
    logger.error(f"Error initializing Kafka producer: {str(e)}")
    producer = None

def novo_cliente(cliente):
    try:
        if producer:
            future = producer.send('user-events', {
                'event_type': 'novo_cliente',
                'data': cliente
            })
            # Add logging and wait for the message to be sent
            result = future.get(timeout=60)
            logger.info(f"Cliente event sent successfully. Topic: {result.topic}, Partition: {result.partition}, Offset: {result.offset}")
        else:
            logger.error("Producer not initialized")
    except Exception as e:
        logger.error(f"Error sending cliente event: {str(e)}")

def novo_vendedor(vendedor):
    try:
        if producer:
            future = producer.send('user-events', {
                'event_type': 'novo_vendedor',
                'data': vendedor
            })
            # Add logging and wait for the message to be sent
            result = future.get(timeout=60)
            logger.info(f"Vendedor event sent successfully. Topic: {result.topic}, Partition: {result.partition}, Offset: {result.offset}")
        else:
            logger.error("Producer not initialized")
    except Exception as e:
        logger.error(f"Error sending vendedor event: {str(e)}")

def novo_produto(produto):
    try:
        if producer:
            future = producer.send('product-events', {
                'event_type': 'novo_produto',
                'data': produto
            })
            # Add logging and wait for the message to be sent
            result = future.get(timeout=60)
            logger.info(f"Produto event sent successfully. Topic: {result.topic}, Partition: {result.partition}, Offset: {result.offset}")
        else:
            logger.error("Producer not initialized")
    except Exception as e:
        logger.error(f"Error sending produto event: {str(e)}")

def novo_pedido(pedido):
    try:
        if producer:
            future = producer.send('order-events', {
                'event_type': 'novo_pedido',
                'data': pedido
            })
            # Add logging and wait for the message to be sent
            result = future.get(timeout=60)
            logger.info(f"Pedido event sent successfully. Topic: {result.topic}, Partition: {result.partition}, Offset: {result.offset}")
        else:
            logger.error("Producer not initialized")
    except Exception as e:
        logger.error(f"Error sending pedido event: {str(e)}")
