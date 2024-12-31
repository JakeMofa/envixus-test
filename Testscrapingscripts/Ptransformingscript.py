import csv
import json
from collections import defaultdict

# Load column mapping JSON
column_mapping = {
    "listing_years": {"year": "Listing Year"},
    "colors": {"name": "Color Name"},
    "makes": {"name": "Make Name"},
    "engine_types": {"name": "Engine Type"},
    "body_types": {"name": "Body Type"},
    "doors": {"number_of_doors": "Number of Doors"},
    "seats": {"number_of_seats": "Number of Seats"},
    "transmissions": {"type": "Transmission Type"},
    "drive_trains": {"type": "Drive Train"},
    "fuel_types": {"name": "Fuel Type"},
    "title_statuses": {"status": "Title Status"},
    "conditions": {"type": "Condition"},
    "locations": {
        "state": "State",
        "city": "City",
        "county": "County",
        "zipcode": "Zip Code",
        "region": "Region",
    },
    "models": {"make_id": "Make Name", "name": "Model Name"},
    "trims": {"model_id": "Model Name", "name": "Trim Name", "description": "Trim Description"},
    "engines": {
        "engine_type_id": "Engine Type",
        "cylinders": "Cylinders",
        "engine_size_l": "Engine Size (L)",
        "horsepower": "Horsepower",
    },
    "manufacturing_years": {"year": "Manufacturing Year"},
    "epa_metrics": {
        "epa_combined_mpg": "EPA Combined MPG",
        "epa_city_mpg": "EPA City MPG",
        "epa_highway_mpg": "EPA Highway MPG",
        "epa_electric_range_mi": "EPA Electric Range (Mi)",
        "epa_time_to_charge_240v_hr": "EPA Time to Charge (Hr)",
        "battery_capacity_kwh": "Battery Capacity (kWh)",
    },
    "torque": {"torque_ft_lbs": "Torque (Ft-Lbs)", "torque_rpm": "Torque (RPM)"},
    "base_vehicles": {
        "make_id": "Make Name",
        "model_id": "Model Name",
        "trim_id": "Trim Name",
        "manufacture_year_id": "Manufacturing Year",
        "exterior_color_id": "Exterior Color",
        "interior_color_id": "Interior Color",
        "body_type_id": "Body Type",
        "door_id": "Number of Doors",
        "seat_id": "Number of Seats",
        "engine_id": "Engine Type",
        "transmission_id": "Transmission Type",
        "drive_train_id": "Drive Train",
        "fuel_type_id": "Fuel Type",
        "fuel_tank_capacity_gal": "Fuel Tank Capacity",
    },
    "vehicles": {
        "base_vehicle_id": "Base Vehicle",
        "vin": "VIN",
        "price": "Price",
        "msrp": "MSRP",
        "mileage": "Mileage",
        "listing_year_id": "Listing Year",
        "condition_id": "Condition",
        "days_on_market": "Days on Market",
        "date_captured": "Date Captured",
        "date_added": "Date Added",
        "date_modified": "Date Modified",
        "accidents_reported": "Accidents Reported",
        "owner_count": "Owner Count",
        "rental_use": "Rental Use",
    },
}

# Load CSV and transform
def transform_data(csv_file, mapping):
    transformed_data = defaultdict(list)
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for table, fields in mapping.items():
                record = {}
                for db_col, csv_col in fields.items():
                    record[db_col] = row.get(csv_col, None)
                transformed_data[table].append(record)
    return transformed_data

# Example usage
csv_file = "sample_data.csv"  # Replace with your CSV file
transformed_data = transform_data(csv_file, column_mapping)

# Output transformed data
for table, records in transformed_data.items():
    print(f"Table: {table}")
    for record in records:
        print(record)
