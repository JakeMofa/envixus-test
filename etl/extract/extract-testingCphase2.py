import requests
import time
from utils.mongo_config import mongo_collection, mongo_client, MONGO_DB_NAME
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DETAILS_COLLECTION_NAME = os.getenv("MONGO_DETAILS_COLLECTION_NAME")
if not DETAILS_COLLECTION_NAME:
    raise ValueError("MONGO_DETAILS_COLLECTION_NAME is not set in .env")

# Connect to the target collection
details_collection = mongo_client[MONGO_DB_NAME][DETAILS_COLLECTION_NAME]

# === Phase 1: Read listing IDs from the listing collection ===
ids_cursor = mongo_collection.find({}, {"id": 1})
ids_list = [doc["id"] for doc in ids_cursor]

print(f"Found {len(ids_list)} listing IDs to process.")

# === Phase 2: Loop through each ID and fetch details ===
for listing_id in ids_list:

    # Deduplication check: skip if this ID already exists in details collection
    existing_count = details_collection.count_documents({
        "$or": [
            {"listingId": listing_id},
            {"listing.id": listing_id}
        ]
    })

    if existing_count > 0:
        print(f"Skipping existing ID: {listing_id}")
        continue

    # Build the details API request
    detail_url = "https://www.cargurus.com/Cars/detailListingJson.action"
    params = {"inventoryListing": listing_id}

    try:
        response = requests.get(detail_url, params=params, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            print(f"Error fetching details for ID {listing_id}: Status {response.status_code}")
            continue

        detail_data = response.json()

        # Normalize by adding top-level listingId
        detail_data["listingId"] = listing_id

        # Insert into MongoDB
        details_collection.insert_one(detail_data)
        print(f"Stored details for ID: {listing_id}")

        # Rate limiting
        time.sleep(1)

    except Exception as e:
        print(f"Exception while processing ID {listing_id}: {e}")

# === Cleanup ===
mongo_client.close()
print("MongoDB connection closed.")
