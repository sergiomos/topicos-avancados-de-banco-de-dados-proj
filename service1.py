import random
from faker import Faker

fake = Faker('pt_BR')

# Gerar clientes com IDs únicos sequenciais
def gerar_clientes(n):
    return [
        {
            'id_cliente': i + 1,
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco': fake.address(),
        }
        for i in range(n)
    ]

# Gerar vendedores com IDs únicos sequenciais
def gerar_vendedores(n):
    return [
        {
            'id_vendedor': i + 1,
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
        }
        for i in range(n)
    ]

# Gerar produtos com IDs únicos sequenciais
def gerar_produtos(n):
    return [
        {
            'id_produto': i + 1,
            'nome': fake.word(),
            'descricao': fake.text(max_nb_chars=100),
            'preco': round(random.uniform(10, 1000), 2),
        }
        for i in range(n)
    ]

# Gerar pedidos que referenciam IDs existentes
def gerar_pedidos(n, clientes, vendedores, produtos):
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

# Função principal de geração
def gerar_dados(qtd_clientes, qtd_vendedores, qtd_produtos, qtd_pedidos):
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

# Teste
dados = gerar_dados(10, 5, 15, 20)

# Exemplo: imprimir os pedidos com os IDs referenciando os dados anteriores
for pedido in dados['pedidos']:
    print(pedido)
