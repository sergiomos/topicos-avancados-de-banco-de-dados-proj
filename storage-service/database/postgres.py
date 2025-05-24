import psycopg2
from psycopg2 import pool
import logging

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append('/home/sergiomos/dev/topicos-avancados-de-banco-de-dados-proj/storage-service/config.py')

from config import POSTGRES_CONFIG


logger = logging.getLogger(__name__)

class PostgresConnection:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        """Initialize the connection pool"""
        try:
            cls._connection_pool = pool.SimpleConnectionPool(
                1,  # minconn
                10,  # maxconn
                host=POSTGRES_CONFIG['host'],
                port=POSTGRES_CONFIG['port'],
                database=POSTGRES_CONFIG['database'],
                user=POSTGRES_CONFIG['user'],
                password=POSTGRES_CONFIG['password']
            )
            logger.info("PostgreSQL connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL connection pool: {str(e)}")
            raise

    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._connection_pool is None:
            cls.initialize()
        return cls._connection_pool.getconn()

    @classmethod
    def release_connection(cls, connection):
        """Release a connection back to the pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.putconn(connection)

    @classmethod
    def close_all(cls):
        """Close all connections in the pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            logger.info("All PostgreSQL connections closed")

    @classmethod
    def execute_query(cls, query, params=None):
        """Execute a query and return the results"""
        connection = None
        try:
            connection = cls.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if cursor.description:  # If the query returns data
                    return cursor.fetchall()
                connection.commit()
                return None
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Error executing PostgreSQL query: {str(e)}")
            raise
        finally:
            if connection:
                cls.release_connection(connection) 
