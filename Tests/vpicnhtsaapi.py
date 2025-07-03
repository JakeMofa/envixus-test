import requests,json;
url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/440?format=json';
r = requests.get(url);
print(r.text);		