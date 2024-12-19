import pandas as pd

def clean_and_reformat_data(input_csv, output_csv):
    try:
        print("Starting data cleaning and reformatting...")

        # Read the CSV file
        df = pd.read_csv(input_csv)

        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The input CSV file is empty.")

        # Rename columns to match database schema
        column_mapping = {
            "Make Name": "make_name",
            "Model Name": "model_name",
            "Trim Year": "manufacturing_year",
            "Trim Name": "trim_name",
            "Trim Description": "trim_description",
            "Trim Msrp": "msrp",
            "Trim Invoice": "price",
            "Engine Type": "engine_type",
            "Engine Fuel Type": "fuel_type",
            "Engine Cylinders": "cylinders",
            "Engine Size": "engine_size_l",
            "Engine Horsepower Hp": "horsepower",
            "Engine Torque Ft Lbs": "torque_ft_lbs",
            "Engine Torque Rpm": "torque_rpm",
            "Engine Drive Type": "drive_type",
            "Engine Transmission": "transmission",
            "Body Type": "body_type",
            "Body Doors": "number_of_doors",
            "Body Seats": "number_of_seats",
            "Mileage Combined Mpg": "epa_combined_mpg",
            "Mileage Epa City Mpg": "epa_city_mpg",
            "Mileage Epa Highway Mpg": "epa_highway_mpg",
            "Mileage Range City": "epa_electric_range_mi",
            "Mileage Epa Combined Mpg Electric": "epa_combined_mpg_electric",
            "Mileage Epa City Mpg Electric": "epa_city_mpg_electric",
            "Mileage Epa Highway Mpg Electric": "epa_highway_mpg_electric",
            "Mileage Range Electric": "epa_electric_range_mi_electric",
            "Mileage Epa Kwh 100 Mi Electric": "battery_capacity_kwh",
            "Mileage Epa Time To Charge Hr 240v Electric": "epa_time_to_charge_240v_hr",
            "Trim Created": "date_captured",
            "Trim Modified": "date_modified"
        }

        df.rename(columns=column_mapping, inplace=True)

        # Ensure manufacturing_year and date_modified columns are correctly populated
        df['manufacturing_year'] = pd.to_datetime(df['manufacturing_year'], errors='coerce').dt.year
        df['date_captured'] = pd.to_datetime(df['date_captured'], format='%m/%d/%y, %I:%M %p', errors='coerce')
        df['date_modified'] = df['date_captured']

        # Drop columns not needed for the database
        columns_to_keep = list(column_mapping.values())
        cleaned_df = df[columns_to_keep]

        # Save the cleaned data to a new CSV file
        cleaned_df.to_csv(output_csv, index=False)

        print("Finished data cleaning and reformatting.")
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    input_csv = '/Users/dean/Documents/GitHub/envixus-test/data/carapi-opendatafeed-sample 3.csv'
    output_csv = '/Users/dean/Documents/GitHub/envixus-test/data/cleaned_used_cars_datafeed.csv'
    clean_and_reformat_data(input_csv, output_csv)
