import requests
import pymongo
from utils.mongo_config import mongo_collection

# === Config ===
ZIP = "76131"
DISTANCE = 100
OFFSET = 0
MAX_RESULT = 2

# === Build URL ===
url = "https://www.cargurus.com/Cars/searchResults.action"
params = {
    "zip": ZIP,
    "distance": DISTANCE,
    "maxResults": MAX_RESULT,
    "offset": OFFSET
}

# === Call API ===
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, params=params, headers=headers)

if response.status_code != 200:
    print("Error:", response.status_code)
    exit()

data = response.json()

# === Parse and store IDs in MongoDB ===
for listing in data:
    listing_id = listing.get("id")
    listing_offset = listing.get("offset")
    if listing_id:
        # Check if ID already exists
        if mongo_collection.count_documents({"id": listing_id}) == 0:
            mongo_collection.insert_one({
                "id": listing_id,
                "offset": listing_offset
            })
            print(f"Stored ID: {listing_id} with offset {listing_offset}")
        else:
            print(f"ID already exists: {listing_id}")

