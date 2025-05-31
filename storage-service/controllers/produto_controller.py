import logging
from database.mongodb import MongoDBConnection
from datetime import datetime

logger = logging.getLogger(__name__)

class ProdutoController:
    @staticmethod
    def insert_produto(produto_data: dict) -> bool:
        """
        Insere ou atualiza um produto no MongoDB
        
        Args:
            produto_data (dict): Dados do produto a ser inserido/atualizado
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            # Adiciona timestamps
            produto_data['created_at'] = datetime.utcnow()
            produto_data['updated_at'] = datetime.utcnow()
            
            # Usa upsert para lidar com inserção e atualização
            result = MongoDBConnection.get_collection('produtos').update_one(
                {'id_produto': produto_data['id_produto']},
                {'$set': produto_data},
                upsert=True
            )
            
            logger.info(f"Produto {produto_data['id_produto']} inserido/atualizado com sucesso no MongoDB")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inserir produto no MongoDB: {str(e)}")
            return False

    @staticmethod
    def get_produto_by_id(produto_id: str) -> dict:
        """
        Obtém um produto pelo seu ID do MongoDB
        
        Args:
            produto_id (str): ID do produto a ser buscado
            
        Returns:
            dict: Dados do produto se encontrado, None caso contrário
        """
        try:
            produto = MongoDBConnection.get_collection('produtos').find_one(
                {'id_produto': produto_id}
            )
            
            if produto:
                # Converte ObjectId para string para serialização JSON
                produto['_id'] = str(produto['_id'])
                return produto
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar produto no MongoDB: {str(e)}")
            return None 