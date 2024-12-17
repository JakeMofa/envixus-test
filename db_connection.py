import psycopg2
from psycopg2 import sql
from db_config import connection_pool

def connect_to_db():
    print("Starting connection process...")
    try:
        # Get a connection from the connection pool
        connection = connection_pool.getconn()
        cursor = connection.cursor()
        print("Connection to PostgreSQL DB successful")
        
        # Close the cursor and return the connection to the pool
        cursor.close()
        connection_pool.putconn(connection)
        print("Connection to PostgreSQL DB closed")
        
    except Exception as error:
        print(f"Error connecting to PostgreSQL DB: {error}")

if __name__ == "__main__":
    connect_to_db()
