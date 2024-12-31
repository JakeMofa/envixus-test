import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        print("Attempting to connect to the database...")
        conn = psycopg2.connect( 
            user='postgres',
            password='envixus19',
            host='172.26.10.236',  # Replace localhost with server IP
            port='5432',
            database='envixus'
        )
        print("Connected successfully!")
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None

# Attempt to create a connection
connection = create_connection()
if connection:
    connection.close()
    print("Connection closed.")
else:
    print("Failed to connect to the database.")