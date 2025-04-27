from kafka import KafkaConsumer
import json
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            print(f"Received message: {message.value}")
            logger.info(f"Received message: {message.value}")
            
    except Exception as e:
        logger.error(f"Error in consumer: {str(e)}")

def run_consumer():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start() 