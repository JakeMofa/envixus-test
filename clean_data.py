import pandas as pd

def clean_and_reformat_data(input_csv, output_csv):
    try:
        print("Starting data cleaning and reformatting...")

        # Read the CSV file
        df = pd.read_csv(input_csv)

        # Create a new DataFrame with the desired columns
        cleaned_data = {
            'Make': [],
            'Model': [],
            'Year': [],
            'Trim': [],
            'Trim (description)': [],
            'Condition type': [],
            'Base MSRP': [],
            'Price': [],
            'Colors exterior': [],
            'Colors interior': [],
            'Body type': [],
            'Doors': [],
            'Body seats': [],
            'VIN': [],
            'Mileage': [],
            'Cylinders': [],
            'Engine size (L)': [],
            'Horsepower (HP)': [],
            'Torque (ft-lbs)': [],
            'Torque (rpm)': [],
            'Drive terrain': [],
            'Transmission': [],
            'Engine type': [],
            'Fuel type': [],
            'Fuel tank capacity (gal)': [],
            'EPA combined MPG': [],
            'EPA city MPG': [],
            'EPA highway MPG': [],
            'EPA electricity range (mi)': [],
            'EPA time to charge battery (at 240V) (hr)': [],
            'Battery capacity (kWh)': [],
            'Source JSON': [],
            'Source URL': [],
            'Source Name': [],
            'Title status': [],
            'Image URL': [],
            'Region': [],
            'State': [],
            'Accidents reported': [],
            'Owner': [],
            'Rental use?': [],
            'Date captured': [],
            'Date added': [],
            'Date modified': [],
            'Days on market': [],
            'Listing year': []
        }

        # Process each row in the original DataFrame
        for _, row in df.iterrows():
            make = row['brand']
            model_split = str(row['model']).split()
            model = ' '.join(model_split[:-1])
            trim = model_split[-1] if len(model_split) > 1 else 'Unknown'
            year = row['model_year']
            price = str(row['price']).replace('$', '').replace(',', '')
            mileage = str(row['milage']).replace(' mi.', '').replace(',', '')
            
            # Initialize default values
            horsepower = 'Unknown'
            engine_size = 'Unknown'
            cylinders = 'Unknown'
            engine_type = 'Unknown'
            
            # Parse the engine details
            engine_details = str(row['engine']).split()
            if len(engine_details) >= 4:
                horsepower = engine_details[0].replace('HP', '')
                engine_size = engine_details[2].replace('L', '')
                cylinders = engine_details[3][0]
                engine_type = engine_details[4] if len(engine_details) > 4 else 'Unknown'
            
            transmission = 'Automatic' if 'A/T' in str(row['transmission']) else 'Manual'
            fuel_type = row['fuel_type']
            title_status = 'Clean title' if row['clean_title'] == 'Yes' else 'Unknown'
            accidents_reported = 1 if 'accident' in str(row['accident']) else 0

            cleaned_data['Make'].append(make)
            cleaned_data['Model'].append(model)
            cleaned_data['Year'].append(year)
            cleaned_data['Trim'].append(trim)
            cleaned_data['Trim (description)'].append('Unknown')
            cleaned_data['Condition type'].append('Used')
            cleaned_data['Base MSRP'].append('Unknown')
            cleaned_data['Price'].append(price)
            cleaned_data['Colors exterior'].append(row['ext_col'])
            cleaned_data['Colors interior'].append(row['int_col'])
            cleaned_data['Body type'].append('Utility')
            cleaned_data['Doors'].append('Unknown')
            cleaned_data['Body seats'].append('Unknown')
            cleaned_data['VIN'].append('Unknown')
            cleaned_data['Mileage'].append(mileage)
            cleaned_data['Cylinders'].append(cylinders)
            cleaned_data['Engine size (L)'].append(engine_size)
            cleaned_data['Horsepower (HP)'].append(horsepower)
            cleaned_data['Torque (ft-lbs)'].append('Unknown')
            cleaned_data['Torque (rpm)'].append('Unknown')
            cleaned_data['Drive terrain'].append('Unknown')
            cleaned_data['Transmission'].append(transmission)
            cleaned_data['Engine type'].append(engine_type)
            cleaned_data['Fuel type'].append(fuel_type)
            cleaned_data['Fuel tank capacity (gal)'].append('Unknown')
            cleaned_data['EPA combined MPG'].append('Unknown')
            cleaned_data['EPA city MPG'].append('Unknown')
            cleaned_data['EPA highway MPG'].append('Unknown')
            cleaned_data['EPA electricity range (mi)'].append('Unknown')
            cleaned_data['EPA time to charge battery (at 240V) (hr)'].append('Unknown')
            cleaned_data['Battery capacity (kWh)'].append('Unknown')
            cleaned_data['Source JSON'].append('Unknown')
            cleaned_data['Source URL'].append('Unknown')
            cleaned_data['Source Name'].append('Unknown')
            cleaned_data['Title status'].append(title_status)
            cleaned_data['Image URL'].append('Unknown')
            cleaned_data['Region'].append('Unknown')
            cleaned_data['State'].append('Unknown')
            cleaned_data['Accidents reported'].append(accidents_reported)
            cleaned_data['Owner'].append('Unknown')
            cleaned_data['Rental use?'].append('Unknown')
            cleaned_data['Date captured'].append('Unknown')
            cleaned_data['Date added'].append('Unknown')
            cleaned_data['Date modified'].append('Unknown')
            cleaned_data['Days on market'].append('Unknown')
            cleaned_data['Listing year'].append('Unknown')

        # Convert the cleaned data to a DataFrame
        cleaned_df = pd.DataFrame(cleaned_data)

        # Save the cleaned data to a new CSV file
        cleaned_df.to_csv(output_csv, index=False)

        print("Finished data cleaning and reformatting.")
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    input_csv = '/Users/dean/Documents/GitHub/envixus-test/used_cars.csv'
    output_csv = '/Users/dean/Documents/GitHub/envixus-test/cleaned_used_cars.csv'
    clean_and_reformat_data(input_csv, output_csv)
