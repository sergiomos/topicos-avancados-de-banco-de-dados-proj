import logging
from database.postgres import PostgresConnection
from models.cliente import Cliente

logger = logging.getLogger(__name__)

class ClienteController:
    @staticmethod
    def insert_cliente(cliente_data: dict) -> bool:
        """
        Insert or update a client in the database
        Returns True if successful, False otherwise
        """
        try:
            query = """
                INSERT INTO clientes (id_cliente, nome, email, telefone, endereco, ativo)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_cliente) DO UPDATE
                SET nome = EXCLUDED.nome,
                    email = EXCLUDED.email,
                    telefone = EXCLUDED.telefone,
                    endereco = EXCLUDED.endereco,
                    ativo = EXCLUDED.ativo
            """
            
            params = (
                cliente_data['id_cliente'],
                cliente_data['nome'],
                cliente_data['email'],
                cliente_data['telefone'],
                cliente_data['endereco'],
                cliente_data.get('ativo', True)
            )
            
            PostgresConnection.execute_query(query, params)
            logger.info(f"Cliente {cliente_data['id_cliente']} inserted/updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting cliente: {str(e)}")
            return False 