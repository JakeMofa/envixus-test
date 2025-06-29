import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Database connection configuration
DB_CONFIG = {
    "dbname": "envixus_db",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}

# Mapping from raw data fields to database tables and fields
FIELD_MAPPINGS = {
    "makes": {"name": "Make Name"},
    "models": {"name": "Model Name", "make_id": "Make Name"},
    "trims": {"name": "Trim Name", "description": "Trim Description", "model_id": "Model Name"},
    "base_vehicles": {
        "make_id": "Make Name",
        "model_id": "Model Name",
        "trim_id": "Trim Name",
        "manufacture_year_id": "Trim Year"
    },
    "vehicles": {
        "base_vehicle_id": "Base Vehicle",
        "price": "Price",
        "mileage": "Mileage",
        "listing_year_id": "Listing Year",
        "condition_id": "Condition"
    }
}

# Utility to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Extract data from a CSV file
def extract_data(file_path):
    return pd.read_csv(file_path)

# Get or insert reference data and return its ID
def get_or_insert(cursor, table, field, value):
    query = f"SELECT id FROM {table} WHERE {field} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        insert_query = f"INSERT INTO {table} ({field}) VALUES (%s) RETURNING id"
        cursor.execute(insert_query, (value,))
        return cursor.fetchone()[0]

# Transform raw data to match the schema
def transform_data(raw_data, cursor):
    transformed_data = {}

    for table, mappings in FIELD_MAPPINGS.items():
        table_data = []
        for _, row in raw_data.iterrows():
            record = {}
            for db_field, raw_field in mappings.items():
                if raw_field in raw_data.columns:
                    if "_id" in db_field:  # Handle foreign keys
                        record[db_field] = get_or_insert(cursor, table[:-1], "name", row[raw_field])
                    else:
                        record[db_field] = row[raw_field]
            table_data.append(record)
        transformed_data[table] = table_data

    return transformed_data

# Load transformed data into the database
def load_data(transformed_data, cursor):
    for table, records in transformed_data.items():
        if records:
            keys = records[0].keys()
            values = [tuple(record.values()) for record in records]
            query = f"INSERT INTO {table} ({', '.join(keys)}) VALUES %s ON CONFLICT DO NOTHING"
            execute_values(cursor, query, values)

# Main ETL function
def etl_pipeline(file_path):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Step 1: Extract
        raw_data = extract_data(file_path)

        # Step 2: Transform
        transformed_data = transform_data(raw_data, cursor)

        # Step 3: Load
        load_data(transformed_data, cursor)

        conn.commit()
        print("ETL process completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"ETL process failed: {e}")
    finally:
        cursor.close()
        conn.close()

# Run the ETL pipeline
if __name__ == "__main__":
    etl_pipeline("vehicle_data.csv")
