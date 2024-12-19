import psycopg2
from psycopg2 import pool, sql

DB_CONFIG = {
    'dbname': 'envixus',
    'user': 'postgres',
    'password': 'envixus19',
    'host': 'localhost',
    'port': '5432'
}

TEMP_DB_NAME = "temp_envixus"

def create_temp_database():
    """Create a temporary database for validation."""
    try:
        # Connect to the default 'postgres' database
        connection = psycopg2.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database="postgres"  # Always use the default database to create a new one
        )
        connection.autocommit = True  # Ensure autocommit mode is enabled
        cursor = connection.cursor()
        
        # Drop the database if it already exists
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(TEMP_DB_NAME)))
        
        # Create the temporary database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TEMP_DB_NAME)))
        print(f"Temporary database '{TEMP_DB_NAME}' created successfully.")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error creating temporary database: {e}")
        return False

def drop_temp_database():
    try:
        with psycopg2.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database="postgres"
        ) as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(TEMP_DB_NAME)))
                print(f"Temporary database '{TEMP_DB_NAME}' dropped successfully.")
    except Exception as e:
        print(f"Error dropping temporary database: {e}")

def create_temp_db_connection_pool():
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=TEMP_DB_NAME
        )
        print(f"Connection pool for temporary database '{TEMP_DB_NAME}' created successfully.")
        return connection_pool
    except Exception as e:
        print(f"Error creating connection pool for temporary database: {e}")
        return None

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        database=DB_CONFIG['dbname']
    )
    print("Connection pool created successfully")
except Exception as error:
    print("Error while connecting to PostgreSQL", error)
