import requests

# URL de la API
api_url = 'https://car.tlacuache.racing/items/BaseVehicle?limit=1&filter[done][_eq]=false&fields[]=makeCode.name,modelCode.name,yearCode&access_token=tKrvK6V3BmywMvGlBLKJ4bkfqIi1lZWF'

# Request data / Solicitar datos
response = requests.get(api_url)
if response.status_code == 200:
    data = response.json().get('data', [])
    if data:
        vehicle = data[0]  # Tomar el primer resultado
        make = vehicle['makeCode']['name'].lower()
        model = vehicle['modelCode']['name'].lower()
        year = vehicle['yearCode']
        
        # Build the URL/ Construir la URL
        kbb_url = f'https://www.kbb.com/{make}/{model}/{year}/'
        print("URL generated:", kbb_url)
    else:
        print("No data found in the response.")
else:
    print("Error getting data. Status code:", response.status_code)
    
    
    
    #Car make , CArmodel, Caryear, CArfactory msrp, Carlivemarketprice
    
    # 1 So the first step would be getting the api and the parameters to pull these     #Car make , CArmodel, Caryear, CArfactory msrp, Carlivemarketprice
    #2 The second step would be for us to store all of the data and the historical data into  mongodb( for historical data, predictive trends ) Database and  Postgresql(users, structure of frontend)
    #3 Figuring out  a way to match multiple 
    
    