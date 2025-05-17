from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import logging
from ..config import CASSANDRA_CONFIG

logger = logging.getLogger(__name__)

class CassandraConnection:
    _cluster = None
    _session = None

    @classmethod
    def initialize(cls):
        """Initialize the Cassandra connection"""
        try:
            cls._cluster = Cluster(
                contact_points=CASSANDRA_CONFIG['contact_points'],
                port=CASSANDRA_CONFIG['port']
            )
            cls._session = cls._cluster.connect()
            
            # Create keyspace if it doesn't exist
            cls._session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_CONFIG['keyspace']}
                WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
            """)
            
            # Use the keyspace
            cls._session.set_keyspace(CASSANDRA_CONFIG['keyspace'])
            
            logger.info("Cassandra connection initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Cassandra connection: {str(e)}")
            raise

    @classmethod
    def get_session(cls):
        """Get the Cassandra session"""
        if cls._session is None:
            cls.initialize()
        return cls._session

    @classmethod
    def close(cls):
        """Close the Cassandra connection"""
        if cls._session is not None:
            cls._session.shutdown()
        if cls._cluster is not None:
            cls._cluster.shutdown()
        cls._session = None
        cls._cluster = None
        logger.info("Cassandra connection closed")

    @classmethod
    def execute(cls, query, parameters=None):
        """Execute a CQL query"""
        try:
            session = cls.get_session()
            return session.execute(query, parameters or ())
        except Exception as e:
            logger.error(f"Error executing Cassandra query: {str(e)}")
            raise

    @classmethod
    def create_table(cls, table_name, columns):
        """Create a table if it doesn't exist"""
        try:
            session = cls.get_session()
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(columns)}
                )
            """
            session.execute(query)
            logger.info(f"Table {table_name} created or already exists")
        except Exception as e:
            logger.error(f"Error creating Cassandra table: {str(e)}")
            raise 
