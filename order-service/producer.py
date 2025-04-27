from kafka import KafkaProducer
import json

# Inicializando 
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def novo_cliente(cliente: dict):
    producer.send('novo-cliente', cliente)