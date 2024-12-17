import psycopg2
from psycopg2 import pool

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user='postgres',
        password='envixus19',
        host='localhost',
        port='5432',
        database='envixus'
    )
    print("Connection pool created successfully")
except Exception as error:
    print("Error while connecting to PostgreSQL", error)
