from faker import Faker
import random
from .produto import gerar_produtos
from .usuario import gerar_clientes, gerar_vendedores

fake = Faker('pt_BR')

def gerar_pedidos(n, clientes, vendedores, produtos):
    """
    Gera uma lista de pedidos que referenciam IDs existentes
    
    Args:
        n (int): Quantidade de pedidos a serem gerados
        clientes (list): Lista de clientes existentes
        vendedores (list): Lista de vendedores existentes
        produtos (list): Lista de produtos existentes
        
    Returns:
        list: Lista de dicionários contendo os dados dos pedidos
    """
    pedidos = []
    for i in range(n):
        cliente = random.choice(clientes)
        vendedor = random.choice(vendedores)
        produto = random.choice(produtos)
        quantidade = random.randint(1, 5)
        preco_total = produto['preco'] * quantidade

        pedidos.append({
            'id_pedido': i + 1,
            'id_cliente': cliente['id_cliente'],
            'id_vendedor': vendedor['id_vendedor'],
            'id_produto': produto['id_produto'],
            'quantidade': quantidade,
            'preco_total': round(preco_total, 2),
            'data_pedido': fake.date_this_year(),
        })
    return pedidos

def gerar_dados(qtd_clientes, qtd_vendedores, qtd_produtos, qtd_pedidos):
    """
    Função principal que gera todos os dados necessários
    
    Args:
        qtd_clientes (int): Quantidade de clientes a gerar
        qtd_vendedores (int): Quantidade de vendedores a gerar
        qtd_produtos (int): Quantidade de produtos a gerar
        qtd_pedidos (int): Quantidade de pedidos a gerar
        
    Returns:
        dict: Dicionário contendo todas as entidades geradas
    """
    clientes = gerar_clientes(qtd_clientes)
    vendedores = gerar_vendedores(qtd_vendedores)
    produtos = gerar_produtos(qtd_produtos)
    pedidos = gerar_pedidos(qtd_pedidos, clientes, vendedores, produtos)

    return {
        'clientes': clientes,
        'vendedores': vendedores,
        'produtos': produtos,
        'pedidos': pedidos
    } 
