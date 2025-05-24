from faker import Faker
import uuid

fake = Faker('pt_BR')

def random_id():
    return str(uuid.uuid4())

def gerar_cliente():
    return {
         'id_cliente': random_id(),
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco': fake.address(),
            'ativo': True
    }

def gerar_clientes(n):
    return [gerar_cliente() for _i in range(n)]

def gerar_vendedor():
    return {
        'id_vendedor': random_id(),
        'nome': fake.name(),
        'email': fake.email(),
        'telefone': fake.phone_number(),
        'ativo': True
    }

def gerar_vendedores(n):
    return [gerar_vendedor() for _i in range(n)]
