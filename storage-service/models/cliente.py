from pydantic import Field
from typing import Optional, List
from datetime import datetime
from .base import BaseUser

class Cliente(BaseUser):
    """Modelo para clientes"""
    id_cliente: str = Field(..., description="Identificador único do cliente")
    endereco: str = Field(..., description="Endereço completo do cliente")

    class Config:
        collection = "clientes"
        schema_extra = {
            "example": {
                "id_cliente": "550e8400-e29b-41d4-a716-446655440000",
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "telefone": "(11) 99999-9999",
                "endereco": "Rua das Flores, 123 - Centro, São Paulo - SP, 01234-567",
                "ativo": True
            }
        } 
