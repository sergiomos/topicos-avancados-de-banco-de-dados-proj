import os

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'ecommerce'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres')
}

# MongoDB Configuration
MONGODB_CONFIG = {
    'uri': os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/ecommerce')
}

# Cassandra Configuration
CASSANDRA_CONFIG = {
    'contact_points': os.getenv('CASSANDRA_CONTACT_POINTS', 'cassandra').split(','),
    'keyspace': os.getenv('CASSANDRA_KEYSPACE', 'ecommerce'),
    'port': int(os.getenv('CASSANDRA_PORT', '9042'))
}

# Kafka Configuration
KAFKA_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092').split(',')
} 
