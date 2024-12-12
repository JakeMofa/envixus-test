import requests
from bs4 import BeautifulSoup

# Define the make, model, and year directly
make = 'honda'
model = 'civic'
year = 2020

# Build the CarGurus URL
cargurus_url = f'https://www.cargurus.com/Cars/l-Used-{make}-{model}-{year}-c{year}'
print("Generated URL:", cargurus_url)

# Request the CarGurus page
cargurus_response = requests.get(cargurus_url)
if cargurus_response.status_code == 200:
    soup = BeautifulSoup(cargurus_response.content, 'html.parser')
    
    # Extract vehicle data
    cars = soup.find_all('div', class_='listing-row')
    for car in cars:
        make = car.find('h4', class_='listing-title').text.strip()
        model = car.find('span', class_='listing-subtitle').text.strip()
        trim = car.find('span', 'trim').text.strip() if car.find('span', 'trim') else 'N/A'
        trim_description = car.find('span', 'trim-description').text.strip() if car.find('span', 'trim-description') else 'N/A'
        price = car.find('span', 'price').text.strip() if car.find('span', 'price') else 'N/A'
        mileage = car.find('span', 'mileage').text.strip() if car.find('span', 'mileage') else 'N/A'
        msrp = car.find('span', 'msrp').text.strip() if car.find('span', 'msrp') else 'N/A'
        
        print(f'Make: {make}, Model: {model}, Trim: {trim}, Trim Description: {trim_description}, Price: {price}, Mileage: {mileage}, MSRP: {msrp}')
else:
    print("Error fetching the CarGurus page. Status code:", cargurus_response.status_code)