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

    @staticmethod
    def get_cliente_by_id(cliente_id: str) -> dict:
        """
        Get a client by their ID
        Returns the client data if found, None otherwise
        """
        try:
            query = """
                SELECT id_cliente, nome, email, telefone, endereco, ativo
                FROM clientes
                WHERE id_cliente = %s
            """
            
            result = PostgresConnection.execute_query(query, (cliente_id,))
            if result and len(result) > 0:
                return {
                    'id_cliente': result[0][0],
                    'nome': result[0][1],
                    'email': result[0][2],
                    'telefone': result[0][3],
                    'endereco': result[0][4],
                    'ativo': result[0][5]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting cliente by ID: {str(e)}")
            return None 