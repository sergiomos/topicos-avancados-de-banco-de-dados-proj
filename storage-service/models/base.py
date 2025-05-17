from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseUser(BaseModel):
    """Modelo base para usuários (clientes e vendedores)"""
    nome: str = Field(..., description="Nome completo do usuário")
    email: str = Field(..., description="Endereço de email do usuário")
    telefone: str = Field(..., description="Número de telefone do usuário")
    data_criacao: datetime = Field(default_factory=datetime.utcnow, description="Data de criação do usuário")
    data_atualizacao: Optional[datetime] = Field(None, description="Data da última atualização")
    ativo: bool = Field(default=True, description="Indica se o usuário está ativo")

    class Config:
        schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "telefone": "(11) 99999-9999",
                "ativo": True
            }
        } 
