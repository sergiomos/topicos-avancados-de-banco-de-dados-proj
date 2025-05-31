import logging
from database.mongodb import MongoDBConnection
from datetime import datetime

logger = logging.getLogger(__name__)

class ProdutoController:
    @staticmethod
    def insert_produto(produto_data: dict) -> bool:
        """
        Insert or update a product in MongoDB
        Returns True if successful, False otherwise
        """
        try:
            # Add timestamps
            produto_data['created_at'] = datetime.utcnow()
            produto_data['updated_at'] = datetime.utcnow()
            
            # Use upsert to handle both insert and update
            result = MongoDBConnection.get_collection('produtos').update_one(
                {'id_produto': produto_data['id_produto']},
                {'$set': produto_data},
                upsert=True
            )
            
            logger.info(f"Produto {produto_data['id_produto']} inserted/updated successfully in MongoDB")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting produto in MongoDB: {str(e)}")
            return False

    @staticmethod
    def get_produto_by_id(produto_id: str) -> dict:
        """
        Get a product by its ID from MongoDB
        Returns the product data if found, None otherwise
        """
        try:
            produto = MongoDBConnection.get_collection('produtos').find_one(
                {'id_produto': produto_id}
            )
            
            if produto:
                # Convert ObjectId to string for JSON serialization
                produto['_id'] = str(produto['_id'])
                return produto
            return None
            
        except Exception as e:
            logger.error(f"Error getting produto from MongoDB: {str(e)}")
            return None 