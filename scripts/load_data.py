import pandas as pd
import json
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from db_config import DB_CONFIG, TEMP_DB_NAME, create_temp_database, drop_temp_database, create_temp_db_connection_pool

def load_column_mapping(json_file="Colmappinng.json"):
    with open(json_file, "r") as file:
        return json.load(file)

def map_csv_to_db(csv_row, mapping, table_name):
    table_mapping = mapping.get(table_name, {})
    mapped_data = {}
    for db_field, csv_field in table_mapping.items():
        value = csv_row.get(csv_field)
        if pd.isna(value):
            if isinstance(value, (int, float)):
                mapped_data[db_field] = None
            else:
                mapped_data[db_field] = 'UNKNOWN'
        else:
            mapped_data[db_field] = value
    return mapped_data

def save_cleaned_csv(df, output_file="cleanedps_csv.csv"):
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

def get_or_create(table, session, **kwargs):
    try:
        instance = session.query(table).filter_by(**kwargs).first()
        if instance:
            print(f"Record already exists in {table.name}: {kwargs}")
            return instance.id
        else:
            result = session.execute(table.insert().values(**kwargs))
            session.commit()
            print(f"New record inserted into {table.name}: {kwargs}")
            return result.inserted_primary_key[0]
    except Exception as e:
        print(f"Error in get_or_create for table {table.name} with data {kwargs}: {e}")
        raise

def preprocess_csv(df, column_mapping):
    # Add missing columns with default values
    for table_name, mapping in column_mapping.items():
        for db_field, csv_field in mapping.items():
            if csv_field not in df.columns:
                # Default values for missing columns
                if isinstance(db_field, int):  # Numeric fields
                    df[csv_field] = None
                else:  # Non-numeric fields
                    df[csv_field] = "UNKNOWN"
                print(f"Added missing column '{csv_field}' with default values.")
    return df

def validate_csv(df, column_mapping):
    for table_name, mapping in column_mapping.items():
        for db_field, csv_field in mapping.items():
            if csv_field not in df.columns:
                raise ValueError(f"Missing column {csv_field} for table {table_name} in CSV.")
    print("CSV validation passed.")

def insert_vehicle_if_not_exists(session, vehicles_table, vehicle_data):
    existing_vehicle = session.query(vehicles_table).filter_by(base_vehicle_id=vehicle_data['base_vehicle_id']).first()
    if not existing_vehicle:
        session.execute(vehicles_table.insert().values(**vehicle_data))
        session.commit()

def add_default_sources(session, sources_table):
    source_data = {
        'name': 'Car API',
        'source_url': 'https://carapi.app/pricing/data-feed#'
    }
    get_or_create(sources_table, session, **source_data)

def load_data_to_temp_db(cleaned_csv):
    if create_temp_database():
        temp_db_pool = create_temp_db_connection_pool()
        column_mapping = load_column_mapping()
        
        if temp_db_pool:
            session = None
            try:
                connection = temp_db_pool.getconn()
                engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{TEMP_DB_NAME}")
                metadata = MetaData()
                metadata.reflect(bind=engine)
                Session = sessionmaker(bind=engine)
                session = Session()

                df = pd.read_csv(cleaned_csv)
                df = preprocess_csv(df, column_mapping)  # Preprocess CSV
                validate_csv(df, column_mapping)  # Validate after preprocessing

                # Define tables
                makes_table = Table('makes', metadata, autoload_with=engine)
                models_table = Table('models', metadata, autoload_with=engine)
                trims_table = Table('trims', metadata, autoload_with=engine)
                engines_table = Table('engines', metadata, autoload_with=engine)
                body_types_table = Table('body_types', metadata, autoload_with=engine)
                doors_table = Table('doors', metadata, autoload_with=engine)
                seats_table = Table('seats', metadata, autoload_with=engine)
                transmissions_table = Table('transmissions', metadata, autoload_with=engine)
                drive_trains_table = Table('drive_trains', metadata, autoload_with=engine)
                fuel_types_table = Table('fuel_types', metadata, autoload_with=engine)
                vehicles_table = Table('vehicles', metadata, autoload_with=engine)
                sources_table = Table('sources', metadata, autoload_with=engine)

                # Insert data into sources
                add_default_sources(session, sources_table)

                vehicle_data_list = []

                for _, row in df.iterrows():
                    row_dict = row.to_dict()
                    make_data = map_csv_to_db(row_dict, column_mapping, "makes")
                    print(f"Processing make: {make_data}")
                    make_id = get_or_create(makes_table, session, **make_data)
                    
                    model_data = map_csv_to_db(row_dict, column_mapping, "models")
                    model_data['make_id'] = make_id
                    model_id = get_or_create(models_table, session, **model_data)
                    
                    trim_data = map_csv_to_db(row_dict, column_mapping, "trims")
                    trim_data['model_id'] = model_id
                    trim_id = get_or_create(trims_table, session, **trim_data)
                    
                    engine_data = map_csv_to_db(row_dict, column_mapping, "engines")
                    engine_id = get_or_create(engines_table, session, **engine_data)
                    
                    body_type_data = map_csv_to_db(row_dict, column_mapping, "body_types")
                    body_type_id = get_or_create(body_types_table, session, **body_type_data)
                    
                    door_data = map_csv_to_db(row_dict, column_mapping, "doors")
                    door_id = get_or_create(doors_table, session, **door_data)
                    
                    seat_data = map_csv_to_db(row_dict, column_mapping, "seats")
                    seat_id = get_or_create(seats_table, session, **seat_data)
                    
                    transmission_data = map_csv_to_db(row_dict, column_mapping, "transmissions")
                    transmission_id = get_or_create(transmissions_table, session, **transmission_data)
                    
                    drive_train_data = map_csv_to_db(row_dict, column_mapping, "drive_trains")
                    drive_train_id = get_or_create(drive_trains_table, session, **drive_train_data)
                    
                    fuel_type_data = map_csv_to_db(row_dict, column_mapping, "fuel_types")
                    fuel_type_id = get_or_create(fuel_types_table, session, **fuel_type_data)

                    vehicle_data = map_csv_to_db(row_dict, column_mapping, "vehicles")
                    vehicle_data.update({
                        'make_id': make_id,
                        'model_id': model_id,
                        'trim_id': trim_id,
                        'engine_id': engine_id,
                        'body_type_id': body_type_id,
                        'door_id': door_id,
                        'seat_id': seat_id,
                        'transmission_id': transmission_id,
                        'drive_train_id': drive_train_id,
                        'fuel_type_id': fuel_type_id,
                        'listing_year': 2023  # Ensure listing year is added
                    })
                    vehicle_data_list.append(vehicle_data)

                session.bulk_insert_mappings(vehicles_table, vehicle_data_list)
                session.commit()

                print("Data loaded into temporary database for validation.")
            except Exception as e:
                print(f"Error loading data to temporary database: {e}")
                session.rollback()
            finally:
                if session:
                    session.close()
                temp_db_pool.putconn(connection)

        validation = input("Is everything validated? (Yes/No): ")
        if validation.lower() == 'yes':
            print("Data is validated. Proceed to load into final database.")
        else:
            drop_temp_database()
            print("Validation failed. Temporary database dropped.")
    else:
        print("Failed to create temporary database. Aborting data load.")

def load_data_to_final_db(cleaned_csv):
    session = None
    try:
        print("Starting data loading to final database...")

        df = pd.read_csv(cleaned_csv)
        df = preprocess_csv(df)  # Preprocess the CSV
        db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
        engine = create_engine(db_url)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Define tables
        makes_table = Table('makes', metadata, autoload_with=engine)
        models_table = Table('models', metadata, autoload_with=engine)
        trims_table = Table('trims', metadata, autoload_with=engine)
        engines_table = Table('engines', metadata, autoload_with=engine)
        body_types_table = Table('body_types', metadata, autoload_with=engine)
        doors_table = Table('doors', metadata, autoload_with=engine)
        seats_table = Table('seats', metadata, autoload_with=engine)
        transmissions_table = Table('transmissions', metadata, autoload_with=engine)
        drive_trains_table = Table('drive_trains', metadata, autoload_with=engine)
        fuel_types_table = Table('fuel_types', metadata, autoload_with=engine)
        vehicles_table = Table('vehicles', metadata, autoload_with=engine)
        sources_table = Table('sources', metadata, autoload_with=engine)

        # Insert data into sources
        add_default_sources(session, sources_table)

        vehicle_data_list = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            make_data = map_csv_to_db(row_dict, column_mapping, "makes")
            print(f"Processing make: {make_data}")
            make_id = get_or_create(makes_table, session, **make_data)
            
            model_data = map_csv_to_db(row_dict, column_mapping, "models")
            model_data['make_id'] = make_id
            model_id = get_or_create(models_table, session, **model_data)
            
            trim_data = map_csv_to_db(row_dict, column_mapping, "trims")
            trim_data['model_id'] = model_id
            trim_id = get_or_create(trims_table, session, **trim_data)
            
            engine_data = map_csv_to_db(row_dict, column_mapping, "engines")
            engine_id = get_or_create(engines_table, session, **engine_data)
            
            body_type_data = map_csv_to_db(row_dict, column_mapping, "body_types")
            body_type_id = get_or_create(body_types_table, session, **body_type_data)
            
            door_data = map_csv_to_db(row_dict, column_mapping, "doors")
            door_id = get_or_create(doors_table, session, **door_data)
            
            seat_data = map_csv_to_db(row_dict, column_mapping, "seats")
            seat_id = get_or_create(seats_table, session, **seat_data)
            
            transmission_data = map_csv_to_db(row_dict, column_mapping, "transmissions")
            transmission_id = get_or_create(transmissions_table, session, **transmission_data)
            
            drive_train_data = map_csv_to_db(row_dict, column_mapping, "drive_trains")
            drive_train_id = get_or_create(drive_trains_table, session, **drive_train_data)
            
            fuel_type_data = map_csv_to_db(row_dict, column_mapping, "fuel_types")
            fuel_type_id = get_or_create(fuel_types_table, session, **fuel_type_data)

            vehicle_data = map_csv_to_db(row_dict, column_mapping, "vehicles")
            vehicle_data.update({
                'make_id': make_id,
                'model_id': model_id,
                'trim_id': trim_id,
                'engine_id': engine_id,
                'body_type_id': body_type_id,
                'door_id': door_id,
                'seat_id': seat_id,
                'transmission_id': transmission_id,
                'drive_train_id': drive_train_id,
                'fuel_type_id': fuel_type_id,
                'listing_year': 2023  # Ensure listing year is added
            })
            vehicle_data_list.append(vehicle_data)

        session.bulk_insert_mappings(vehicles_table, vehicle_data_list)
        session.commit()

        print("Finished data loading to final database.")
    except Exception as e:
        print(f"Something went wrong: {e}")
        session.rollback()
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    cleaned_csv = '/Users/dean/Documents/GitHub/envixus-test/data/cleaned_used_cars_datafeed.csv'

    # Load data to temporary database
    load_data_to_temp_db(cleaned_csv)

    # Prompt user for validation
    validation = input("Is everything validated? (Yes/No): ")
    if validation.lower() == 'yes':
        # Load data to final database
        load_data_to_final_db(cleaned_csv)
    else:
        print("Data validation failed. Please review and correct the data.")
