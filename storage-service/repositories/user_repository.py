from typing import Optional, List, Type, TypeVar
from datetime import datetime
from database import MongoDBConnection
from models import Cliente, Vendedor

T = TypeVar('T', Cliente, Vendedor)

class UserRepository:
    """Repositório para operações de usuários (clientes e vendedores) no MongoDB"""
    
    @staticmethod
    async def create_user(user: T) -> str:
        """
        Cria um novo usuário no MongoDB
        
        Args:
            user: Instância de Cliente ou Vendedor
            
        Returns:
            str: ID do usuário criado
        """
        user_dict = user.dict()
        user_dict['data_criacao'] = datetime.utcnow()
        
        collection_name = user.Config.collection
        return MongoDBConnection.insert_one(collection_name, user_dict)

    @staticmethod
    async def get_user(user_id: str, user_type: Type[T]) -> Optional[T]:
        """
        Obtém um usuário pelo ID
        
        Args:
            user_id: ID do usuário
            user_type: Tipo do usuário (Cliente ou Vendedor)
            
        Returns:
            Optional[T]: Instância do usuário se encontrado, None caso contrário
        """
        collection_name = user_type.Config.collection
        id_field = 'id_cliente' if user_type == Cliente else 'id_vendedor'
        user_dict = MongoDBConnection.find_one(collection_name, {id_field: user_id})
        
        if user_dict:
            return user_type(**user_dict)
        return None

    @staticmethod
    async def update_user(user_id: str, user: T) -> bool:
        """
        Atualiza as informações de um usuário
        
        Args:
            user_id: ID do usuário
            user: Instância atualizada do usuário
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        user_dict = user.dict()
        user_dict['data_atualizacao'] = datetime.utcnow()
        
        collection_name = user.Config.collection
        id_field = 'id_cliente' if isinstance(user, Cliente) else 'id_vendedor'
        result = MongoDBConnection.get_collection(collection_name).update_one(
            {id_field: user_id},
            {'$set': user_dict}
        )
        
        return result.modified_count > 0

    @staticmethod
    async def delete_user(user_id: str, user_type: Type[T]) -> bool:
        """
        Exclui um usuário (soft delete - marca como inativo)
        
        Args:
            user_id: ID do usuário
            user_type: Tipo do usuário (Cliente ou Vendedor)
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        collection_name = user_type.Config.collection
        id_field = 'id_cliente' if user_type == Cliente else 'id_vendedor'
        result = MongoDBConnection.get_collection(collection_name).update_one(
            {id_field: user_id},
            {'$set': {'ativo': False, 'data_atualizacao': datetime.utcnow()}}
        )
        
        return result.modified_count > 0

    @staticmethod
    async def list_users(user_type: Type[T], skip: int = 0, limit: int = 10) -> List[T]:
        """
        Lista usuários com paginação
        
        Args:
            user_type: Tipo do usuário (Cliente ou Vendedor)
            skip: Número de registros para pular
            limit: Número máximo de registros a retornar
            
        Returns:
            List[T]: Lista de instâncias de usuários
        """
        collection_name = user_type.Config.collection
        cursor = MongoDBConnection.get_collection(collection_name).find(
            {'ativo': True}
        ).skip(skip).limit(limit)
        
        return [user_type(**doc) for doc in cursor] 
