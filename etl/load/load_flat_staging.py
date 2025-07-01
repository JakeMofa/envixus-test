import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sqlalchemy import create_engine
from utils.db_config import DB_CONFIG

def load_flat_staging_table(cleaned_csv):
    print(f"\nStarting load process for: {cleaned_csv}")

    # Read the cleaned CSV
    print("Reading cleaned CSV file...")
    df = pd.read_csv(cleaned_csv)
    print(f"CSV loaded with {len(df)} rows.")

    # Build database URL
    db_url = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )

    print("Connecting to PostgreSQL database...")
    engine = create_engine(db_url)
    connection = engine.connect()
    print("Database connection opened.")

    try:
        # Load into PostgreSQL table
        print("Inserting data into vehicle_flat_staging table...")
        df.to_sql(
            name="vehicle_flat_staging",
            con=connection,
            if_exists="append",
            index=False
        )
        print("Data successfully loaded into vehicle_flat_staging.")
    except Exception as e:
        print(f"ERROR during data load: {e}")
    finally:
        connection.close()
        print("Database connection closed.\n")

if __name__ == "__main__":
    cleaned_csv = "./data/cleaned/vehicle_flat_staging.csv"
    load_flat_staging_table(cleaned_csv)
