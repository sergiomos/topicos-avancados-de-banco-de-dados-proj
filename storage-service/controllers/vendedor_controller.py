import logging
from database.postgres import PostgresConnection
from models.vendedor import Vendedor

logger = logging.getLogger(__name__)

class VendedorController:
    @staticmethod
    def insert_vendedor(vendedor_data: dict) -> bool:
        """
        Insert or update a vendedor in the database
        Returns True if successful, False otherwise
        """
        try:
            query = """
                INSERT INTO vendedores (id_vendedor, nome, email, telefone, ativo)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_vendedor) DO UPDATE
                SET nome = EXCLUDED.nome,
                    email = EXCLUDED.email,
                    telefone = EXCLUDED.telefone,
                    ativo = EXCLUDED.ativo
            """
            
            params = (
                vendedor_data['id_vendedor'],
                vendedor_data['nome'],
                vendedor_data['email'],
                vendedor_data['telefone'],
                vendedor_data.get('ativo', True)
            )
            
            PostgresConnection.execute_query(query, params)
            logger.info(f"Vendedor {vendedor_data['id_vendedor']} inserted/updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting vendedor: {str(e)}")
            return False 