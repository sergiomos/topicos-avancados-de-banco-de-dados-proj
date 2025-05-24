import logging
from database.postgres import PostgresConnection

logger = logging.getLogger(__name__)

def init_database():
    """Initialize all database tables"""
    try:
        # Create clientes table
        create_clientes_table = """
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente UUID PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                telefone VARCHAR(20) NOT NULL,
                endereco TEXT NOT NULL,
                ativo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email);
            CREATE INDEX IF NOT EXISTS idx_clientes_nome ON clientes(nome);
        """

        # Create vendedores table
        create_vendedores_table = """
            CREATE TABLE IF NOT EXISTS vendedores (
                id_vendedor UUID PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                telefone VARCHAR(20) NOT NULL,
                ativo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_vendedores_email ON vendedores(email);
            CREATE INDEX IF NOT EXISTS idx_vendedores_nome ON vendedores(nome);
        """

        # Create update timestamp function
        create_update_timestamp_function = """
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """

        # Create triggers
        create_triggers = """
            DROP TRIGGER IF EXISTS update_clientes_updated_at ON clientes;
            CREATE TRIGGER update_clientes_updated_at
                BEFORE UPDATE ON clientes
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();

            DROP TRIGGER IF EXISTS update_vendedores_updated_at ON vendedores;
            CREATE TRIGGER update_vendedores_updated_at
                BEFORE UPDATE ON vendedores
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
        """

        # Execute all SQL statements
        PostgresConnection.execute_query(create_update_timestamp_function)
        PostgresConnection.execute_query(create_clientes_table)
        PostgresConnection.execute_query(create_vendedores_table)
        PostgresConnection.execute_query(create_triggers)

        logger.info("Database tables initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False 