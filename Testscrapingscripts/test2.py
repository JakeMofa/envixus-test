import requests
from bs4 import BeautifulSoup

# Define the make, model, and year directly
make = 'honda'
model = 'civic'
year = 2020
zipcode = '90210'  # Example ZIP code

# Build the CarGurus search URL
search_url = f'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip={zipcode}&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&entitySelectingHelper.selectedEntity=d{year}&entitySelectingHelper.selectedEntity2=m{model}&entitySelectingHelper.selectedEntity3=m{make}&entitySelectingHelper.selectedEntity4=m{year}'
print("Generated search URL:", search_url)

# Request the CarGurus search page
search_response = requests.get(search_url)
if search_response.status_code == 200:
    search_soup = BeautifulSoup(search_response.content, 'html.parser')
    
    # Find the first car in the search results
    first_car = search_soup.find('a', class_='cg-dealFinder-result-stats')
    if first_car:
        car_url = 'https://www.cargurus.com' + first_car['href']
        print("First car URL:", car_url)
        
        # Request the car details page
        car_response = requests.get(car_url)
        if car_response.status_code == 200:
            car_soup = BeautifulSoup(car_response.content, 'html.parser')
            
            # Extract vehicle data from the details page
            make = car_soup.find('h1', class_='cui-heading-2--secondary').text.strip()
            model = car_soup.find('h1', class_='cui-heading-2--secondary').text.strip()
            trim = car_soup.find('span', class_='trim').text.strip() if car_soup.find('span', 'trim') else 'N/A'
            trim_description = car_soup.find('span', 'trim-description').text.strip() if car_soup.find('span', 'trim-description') else 'N/A'
            price = car_soup.find('span', 'price').text.strip() if car_soup.find('span', 'price') else 'N/A'
            mileage = car_soup.find('span', 'mileage').text.strip() if car_soup.find('span', 'mileage') else 'N/A'
            msrp = car_soup.find('span', 'msrp').text.strip() if car_soup.find('span', 'msrp') else 'N/A'
            
            print(f'Make: {make}, Model: {model}, Trim: {trim}, Trim Description: {trim_description}, Price: {price}, Mileage: {mileage}, MSRP: {msrp}')
        else:
            print("Error fetching the car details page. Status code:", car_response.status_code)
    else:
        print("No cars found in the search results.")
else:
    print("Error fetching the CarGurus search page. Status code:", search_response.status_code)