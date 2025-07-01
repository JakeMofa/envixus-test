import pandas as pd

def transform_carapi_csv(input_csv, output_csv):
    try:
        print("Starting CarAPI data transformation...")

        # Read the CSV file
        df = pd.read_csv(input_csv)
        if df.empty:
            raise ValueError("The input CSV file is empty.")

        # Mapping of CarAPI CSV columns to staging table columns
        column_mapping = {
            "Make Name": "make",
            "Model Name": "model",
            "Trim Year": "manufacturing_year",
            "Trim Name": "trim_name",
            "Trim Description": "trim_description",
            "Trim Msrp": "base_msrp",
            "Trim Invoice": "price",
            "Engine Type": "engine_type",
            "Engine Fuel Type": "fuel_type",
            "Engine Cylinders": "engine_cylinders",
            "Engine Size": "engine_size_l",
            "Engine Horsepower Hp": "horsepower",
            "Engine Torque Ft Lbs": "torque_ft_lbs",
            "Engine Torque Rpm": "torque_rpm",
            "Engine Drive Type": "drive_train",
            "Engine Transmission": "transmission",
            "Body Type": "body_type",
            "Body Doors": "doors",
            "Body Seats": "seats",
            "Mileage Fuel Tank Capacity": "fuel_tank_capacity_gal",
            "Mileage Combined Mpg": "epa_combined_mpg",
            "Mileage Epa City Mpg": "epa_city_mpg",
            "Mileage Epa Highway Mpg": "epa_highway_mpg",
            "Mileage Range City": "epa_electric_range_mi",
            "Mileage Epa Kwh 100 Mi Electric": "battery_capacity_kwh",
            "Mileage Epa Time To Charge Hr 240v Electric": "epa_charge_time_hr",
            "Trim Created": "date_captured",
            "Trim Modified": "date_modified"
        }

        # Rename columns
        df.rename(columns=column_mapping, inplace=True)

        # Ensure dates and years are consistent
        if "manufacturing_year" in df.columns:
            df['manufacturing_year'] = pd.to_numeric(df['manufacturing_year'], errors='coerce').astype('Int64')


        if "date_captured" in df.columns:
            df["date_captured"] = pd.to_datetime(df["date_captured"], format="%m/%d/%y, %I:%M %p",  errors='coerce')
            df["date_modified"] = df["date_captured"]
            
        # Clean engine_cylinders: Remove any leading letters and keep the number
        if "engine_cylinders" in df.columns:
            df["engine_cylinders"] = df["engine_cylinders"].str.extract('(\d+)').astype(float)


        # Add hardcoded source metadata
        df["source_name"] = "carapi"
        df["source_url"] = "https://carapi.app/features/vehicle-csv-download"

        # Add empty/placeholder columns for new staging schema
        df["vin"] = None
        df["listing_year"] = None
        df["region"] = None
        df["state_name"] = None
        df["city"] = None
        df["county"] = None
        df["zipcode"] = None
        df["accidents_reported"] = None
        df["owner_count"] = None
        df["rental_use"] = None
        df["days_on_market"] = None
        df["image_url"] = None
        df["source_json"] = None
        df["source_id"] = None

        # Reorder to match  staging table
        final_columns = [
            "vin", "make", "model", "trim_name", "trim_description",
            "manufacturing_year", "listing_year",
            "condition_type", "base_msrp", "price", "mileage",
            "exterior_color", "interior_color",
            "body_type", "doors", "seats",
            "engine_type", "engine_cylinders", "engine_size_l", "horsepower", "torque_ft_lbs", "torque_rpm",
            "transmission", "drive_train", "fuel_type", "fuel_tank_capacity_gal",
            "epa_combined_mpg", "epa_city_mpg", "epa_highway_mpg", "epa_electric_range_mi",
            "epa_charge_time_hr", "battery_capacity_kwh",
            "region", "state_name", "city", "county", "zipcode",
            "accidents_reported", "owner_count", "rental_use",
            "date_captured", "date_added", "date_modified", "days_on_market",
            "source_name", "source_url", "image_url", "source_json", "source_id"
        ]

        
        for col in final_columns:
            if col not in df.columns:
                df[col] = None

        # Reorder columns
        df = df[final_columns]

        # Save to CSV
        df.to_csv(output_csv, index=False)
        print(f"Finished CarAPI transformation. Cleaned file written to {output_csv}")

    except Exception as e:
        print(f"Error during transformation: {e}")

if __name__ == "__main__":
    input_csv = "./data/raw/carapi-opendatafeed-sample.csv"
    output_csv = "./data/cleaned/vehicle_flat_staging.csv"
    transform_carapi_csv(input_csv, output_csv)
