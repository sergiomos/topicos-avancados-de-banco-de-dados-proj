# E-commerce Database Project

Este projeto é dedicado a construção de um sistema de armazenamento de dados para um e-commerce, utilizando micro-serviços com mensageria e três tipos de bancos de dados:

- **PostgreSQL**: Para armazenar dados de clientes e vendedores.
- **MongoDB**: Para armazenar dados de produtos.
- **Cassandra**: Para armazenar dados de pedidos.

## Arquitetura do Sistema

O sistema é composto por três micro-serviços principais:

1. **Storage Service** (Porta 8081)
   - Gerencia o armazenamento de dados em diferentes bancos
   - Implementa padrão MVC
   - Endpoints para CRUD de clientes, vendedores, produtos e pedidos

2. **Order Service** (Porta 8082)
   - Gerencia o fluxo de pedidos
   - Publica eventos para o Storage Service
   - Endpoints para criação e gerenciamento de pedidos

3. **Log Service** (Porta 8083)
   - Registra todos os eventos do sistema
   - Consome eventos do Kafka
   - Fornece logs detalhados das operações

## Tecnologias Utilizadas

- **Python**: A linguagem principal utilizada para a criação dos serviços e integração com a mensageria e banco de dados.
- **PostgreSQL**: Banco de dados relacional usado para armazenar dados estruturados (clientes, vendedores).
- **MongoDB**: Banco de dados NoSQL utilizado para armazenar dados semi-estruturados (produtos).
- **Cassandra**: Banco de dados NoSQL utilizado para dados de pedidos.
- **Kafka**: Sistema de mensageria para comunicação entre serviços
- **FastAPI**: Framework web para criação das APIs
- **Docker**: Containerização dos serviços e bancos de dados

## Requisitos do Sistema

- Docker e Docker Compose
- Python 3.8 ou superior
- Git
- Mínimo 4GB de RAM disponível
- 10GB de espaço em disco

## Como Iniciar o Projeto

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Inicie os serviços usando Docker Compose:
```bash
docker-compose up -d
```

4. Aguarde todos os serviços iniciarem (pode levar alguns minutos na primeira execução)

5. Verifique se os serviços estão rodando:
```bash
docker-compose ps
```

## Endpoints Disponíveis

Todos os serviços incluem documentação Swagger (OpenAPI) que pode ser acessada através do endpoint `/docs`. Você pode testar todas as rotas diretamente pela interface do Swagger.

### Storage Service (http://localhost:8081)
- Documentação Swagger: http://localhost:8081/docs
- `GET /api/clients/{client_id}` - Busca cliente por ID
- `POST /api/clients` - Cria novo cliente
- `GET /api/sellers/{seller_id}` - Busca vendedor por ID
- `POST /api/sellers` - Cria novo vendedor
- `GET /api/products/{product_id}` - Busca produto por ID
- `POST /api/products` - Cria novo produto
- `GET /api/orders/{order_id}` - Busca pedido por ID
- `POST /api/orders` - Cria novo pedido

### Order Service (http://localhost:8082)
- Documentação Swagger: http://localhost:8082/docs
- `POST /api/orders` - Cria novo pedido
- `GET /api/orders/{order_id}` - Busca pedido por ID
- `GET /api/orders/client/{client_id}` - Lista pedidos por cliente

### Log Service (http://localhost:8083)
- Documentação Swagger: http://localhost:8083/docs
- `GET /health` - Verifica saúde do serviço
- `POST /api/log/event` - Registra novo evento

## Como o Sistema Funciona

1. **Fluxo de Pedidos**:
   - Cliente faz um pedido através do Order Service
   - Order Service publica eventos no Kafka
   - Storage Service consome os eventos e armazena os dados
   - Log Service registra todas as operações

2. **Armazenamento de Dados**:
   - Dados de clientes e vendedores são armazenados no PostgreSQL
   - Produtos são armazenados no MongoDB
   - Pedidos são armazenados no Cassandra

3. **Comunicação entre Serviços**:
   - Kafka é usado como sistema de mensageria
   - Eventos são publicados em tópicos específicos
   - Cada serviço consome apenas os eventos relevantes

## Monitoramento e Logs

- Logs são centralizados no Log Service
- Cada operação é registrada com timestamp e detalhes
- É possível rastrear todo o fluxo de dados através dos logs

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
