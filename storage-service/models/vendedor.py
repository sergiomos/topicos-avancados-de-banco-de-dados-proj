from pydantic import Field
from typing import Optional, List
from datetime import datetime
from .base import BaseUser

class Vendedor(BaseUser):
    """Modelo para vendedores"""
    id_vendedor: str = Field(..., description="Identificador único do vendedor")

    class Config:
        collection = "vendedores"
        schema_extra = {
            "example": {
                "id_vendedor": "550e8400-e29b-41d4-a716-446655440000",
                "nome": "Empresa XYZ",
                "email": "contato@empresaxyz.com",
                "telefone": "(11) 3333-3333",
                "ativo": True
            }
        } 
