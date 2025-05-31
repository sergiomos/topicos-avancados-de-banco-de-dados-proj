import logging
from database.cassandra import CassandraConnection
from datetime import datetime

logger = logging.getLogger(__name__)

class PedidoController:
    @staticmethod
    def insert_pedido(pedido_data: dict) -> bool:
        """
        Insere ou atualiza um pedido no Cassandra
        
        Args:
            pedido_data (dict): Dados do pedido a ser inserido/atualizado
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            # Adiciona timestamps
            pedido_data['created_at'] = datetime.utcnow()
            pedido_data['updated_at'] = datetime.utcnow()
            
            # Prepara os dados do pedido
            order_data = {
                'id_pedido': pedido_data['id_pedido'],
                'id_cliente': pedido_data['id_cliente'],
                'id_vendedor': pedido_data['id_vendedor'],
                'data_pedido': pedido_data['data_pedido'],
                'status': pedido_data['status'],
                'total': pedido_data['total'],
                'created_at': pedido_data['created_at'],
                'updated_at': pedido_data['updated_at']
            }
            
            # Insere o pedido
            session = CassandraConnection.get_session()
            session.execute("""
                INSERT INTO pedidos (
                    id_pedido, id_cliente, id_vendedor, data_pedido, 
                    status, total, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                order_data['id_pedido'],
                order_data['id_cliente'],
                order_data['id_vendedor'],
                order_data['data_pedido'],
                order_data['status'],
                order_data['total'],
                order_data['created_at'],
                order_data['updated_at']
            ))
            
            # Insere os itens do pedido
            for item in pedido_data['itens']:
                session.execute("""
                    INSERT INTO itens_pedido (
                        id_pedido, id_produto, quantidade, 
                        preco_unitario, created_at
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    pedido_data['id_pedido'],
                    item['id_produto'],
                    item['quantidade'],
                    item['preco_unitario'],
                    datetime.utcnow()
                ))
            
            logger.info(f"Pedido {pedido_data['id_pedido']} inserido/atualizado com sucesso no Cassandra")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inserir pedido no Cassandra: {str(e)}")
            return False

    @staticmethod
    def get_pedido_by_id(pedido_id: str) -> dict:
        """
        Obtém um pedido pelo seu ID do Cassandra
        
        Args:
            pedido_id (str): ID do pedido a ser buscado
            
        Returns:
            dict: Dados do pedido com seus itens se encontrado, None caso contrário
        """
        try:
            session = CassandraConnection.get_session()
            
            # Obtém os dados do pedido
            order_result = session.execute("""
                SELECT id_pedido, id_cliente, id_vendedor, data_pedido, 
                       status, total, created_at, updated_at
                FROM pedidos
                WHERE id_pedido = %s
            """, (pedido_id,))
            
            order_row = order_result.one()
            if not order_row:
                return None
                
            # Converte a linha do pedido para dicionário
            order_data = {
                'id_pedido': order_row.id_pedido,
                'id_cliente': order_row.id_cliente,
                'id_vendedor': order_row.id_vendedor,
                'data_pedido': order_row.data_pedido,
                'status': order_row.status,
                'total': order_row.total,
                'created_at': order_row.created_at,
                'updated_at': order_row.updated_at
            }
            
            # Obtém os itens do pedido
            items_result = session.execute("""
                SELECT id_produto, quantidade, preco_unitario, created_at
                FROM itens_pedido
                WHERE id_pedido = %s
            """, (pedido_id,))
            
            # Converte os itens para lista de dicionários
            order_data['itens'] = [
                {
                    'id_produto': item.id_produto,
                    'quantidade': item.quantidade,
                    'preco_unitario': item.preco_unitario,
                    'created_at': item.created_at
                }
                for item in items_result
            ]
            
            return order_data
            
        except Exception as e:
            logger.error(f"Erro ao buscar pedido no Cassandra: {str(e)}")
            return None 