import psycopg2
from db_config import DB_CONFIG

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )
    return conn

if __name__ == "__main__":
    connection = get_db_connection()
    print("Connection to PostgreSQL DB successful")
    connection.close()
    print("Connection to PostgreSQL DB closed")
