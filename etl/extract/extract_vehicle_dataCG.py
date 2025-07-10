import requests
from utils.mongo_config import mongo_collection

# === Config ===
ZIP = "76131"
DISTANCE = 100
OFFSET = 0
MAX_RESULT = 2

# === Ensure unique index on 'id' ===
mongo_collection.create_index("id", unique=True)

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
        # Atomic upsert
        result = mongo_collection.update_one(
            {"id": listing_id},
            {"$setOnInsert": {"id": listing_id, "offset": listing_offset}},
            upsert=True
        )

        if result.upserted_id:
            print(f"Inserted new ID: {listing_id}")
        else:
            print(f"ID already exists: {listing_id}")