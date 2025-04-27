import random
from faker import Faker

fake = Faker('pt_BR')

def gerar_cliente():
    return {
         'id_cliente': fake.random_uuid(),
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco': fake.address(),
    }

def gerar_clientes(n):
    return [gerar_cliente(i) for i in range(n)]

def gerar_vendedor():
    return {
        'id_vendedor': fake.random_uuid(),
        'nome': fake.name(),
        'email': fake.email(),
        'telefone': fake.phone_number(),
    }

def gerar_vendedores(n):
    return [gerar_vendedor() for i in range(n)]
