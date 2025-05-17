from faker import Faker
import random

fake = Faker('pt_BR')

def gerar_produtos(n):
    """
    Gera uma lista de produtos com IDs únicos sequenciais
    
    Args:
        n (int): Quantidade de produtos a serem gerados
        
    Returns:
        list: Lista de dicionários contendo os dados dos produtos
    """
    return [
        {
            'id_produto': i + 1,
            'nome': fake.word(),
            'descricao': fake.text(max_nb_chars=100),
            'preco': round(random.uniform(10, 1000), 2),
        }
        for i in range(n)
    ] 
