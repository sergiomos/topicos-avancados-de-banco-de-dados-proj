from faker import Faker
import uuid

fake = Faker('pt_BR')

def gerar_cliente():
    return {
         'id_cliente': uuid.uuid4(),
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco': fake.address(),
    }

def gerar_clientes(n):
    return [gerar_cliente() for _i in range(n)]

def gerar_vendedor():
    return {
        'id_vendedor': uuid.uuid4(),
        'nome': fake.name(),
        'email': fake.email(),
        'telefone': fake.phone_number(),
    }

def gerar_vendedores(n):
    return [gerar_vendedor() for _i in range(n)]
