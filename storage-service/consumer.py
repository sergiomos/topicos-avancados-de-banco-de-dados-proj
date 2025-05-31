from kafka import KafkaConsumer
import json
import logging
import threading
from controllers.cliente_controller import ClienteController
from controllers.vendedor_controller import VendedorController
from controllers.produto_controller import ProdutoController
from controllers.pedido_controller import PedidoController
from producer import send_storage_response

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_user_event(event_data):
    """
    Processa eventos relacionados a usuários (clientes e vendedores)
    
    Args:
        event_data (dict): Dados do evento recebido
    """
    event_type = event_data.get('event_type')
    if event_type == 'novo_cliente':
        cliente_data = event_data.get('data', {})
        success = ClienteController.insert_cliente(cliente_data)
        send_storage_response(event_type, success, cliente_data)
    elif event_type == 'novo_vendedor': 
        vendedor_data = event_data.get('data', {})
        success = VendedorController.insert_vendedor(vendedor_data)
        send_storage_response(event_type, success, vendedor_data)
    else:
        logger.info(f"Mensagem recebida com tipo de evento: {event_type}")
        send_storage_response(event_type, False, {"error": "Tipo de evento desconhecido"})

def handle_product_event(event_data):
    """
    Processa eventos relacionados a produtos
    
    Args:
        event_data (dict): Dados do evento recebido
    """
    event_type = event_data.get('event_type')
    if event_type == 'novo_produto':
        produto_data = event_data.get('data', {})
        success = ProdutoController.insert_produto(produto_data)
        send_storage_response(event_type, success, produto_data)
    else:
        logger.info(f"Mensagem recebida com tipo de evento: {event_type}")
        send_storage_response(event_type, False, {"error": "Tipo de evento desconhecido"})

def handle_order_event(event_data):
    """
    Processa eventos relacionados a pedidos
    
    Args:
        event_data (dict): Dados do evento recebido
    """
    event_type = event_data.get('event_type')
    if event_type == 'novo_pedido':
        pedido_data = event_data.get('data', {})
        success = PedidoController.insert_pedido(pedido_data)
        send_storage_response(event_type, success, pedido_data)
    else:
        logger.info(f"Mensagem recebida com tipo de evento: {event_type}")
        send_storage_response(event_type, False, {"error": "Tipo de evento desconhecido"})

def start_consumer():
    """
    Inicia os consumidores Kafka para cada tópico e processa as mensagens
    """
    try:
        # Cria consumidores para cada tópico
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
        
        logger.info("Consumidores Kafka iniciados com sucesso")
        
        # Processa mensagens de todos os consumidores
        while True:
            # Processa eventos de usuário
            for message in user_consumer:
                try:
                    event_data = message.value
                    handle_user_event(event_data)
                except Exception as e:
                    logger.error(f"Erro ao processar mensagem de usuário: {str(e)}")
                    send_storage_response("user_event_error", False, {"error": str(e)})
            
            # Processa eventos de produto
            for message in product_consumer:
                try:
                    event_data = message.value
                    handle_product_event(event_data)
                except Exception as e:
                    logger.error(f"Erro ao processar mensagem de produto: {str(e)}")
                    send_storage_response("product_event_error", False, {"error": str(e)})
            
            # Processa eventos de pedido
            for message in order_consumer:
                try:
                    event_data = message.value
                    handle_order_event(event_data)
                except Exception as e:
                    logger.error(f"Erro ao processar mensagem de pedido: {str(e)}")
                    send_storage_response("order_event_error", False, {"error": str(e)})
            
    except Exception as e:
        logger.error(f"Erro no consumidor: {str(e)}")

def run_consumer():
    """
    Inicia o consumidor em uma thread separada
    """
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start() 