import requests
import time
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# === Load environment variables ===
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
LISTING_COLLECTION_NAME = os.getenv("MONGO_LISTING_COLLECTION_NAME")
OFFSET_COLLECTION_NAME = os.getenv("MONGO_OFFSET_COLLECTION_NAME")

# === Setup Mongo ===
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
listing_collection = db[LISTING_COLLECTION_NAME]
offset_collection = db[OFFSET_COLLECTION_NAME]

# === Config ===
ZIP = "76131"
DISTANCE = 100
MAX_RESULTS = 20
TARGET_CAP = None  # or set to 2000 for a limit

# === Offset Tracker ===
offset_doc = offset_collection.find_one({"_id": "offset_tracker"})
if offset_doc is None:
    offset = 0
else:
    offset = offset_doc["last_offset"]

print(f"Starting from offset: {offset}")

# === Loop ===
total_inserted = 0
while True:
    # Stop if cap is reached
    if TARGET_CAP is not None and total_inserted >= TARGET_CAP:
        print(f"Reached target cap of {TARGET_CAP}. Stopping.")
        break

    # === Build URL ===
    url = "https://www.cargurus.com/Cars/searchResults.action"
    params = {
        "zip": ZIP,
        "distance": DISTANCE,
        "maxResults": MAX_RESULTS,
        "offset": offset
    }

    print(f"\nRequesting offset {offset}")
    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    data = response.json()
    if not data:
        print("No more results. Done!")
        break

    # === Process and Insert IDs ===
    count_in_batch = 0
    for listing in data:
        listing_id = listing.get("id")
        listing_offset = offset

        if listing_id:
            doc = {
                "id": listing_id,
                "offset": listing_offset,
                "timestamp": datetime.datetime.utcnow()
            }

            result = listing_collection.update_one(
                {"id": listing_id},
                {"$setOnInsert": doc},
                upsert=True
            )

            if result.upserted_id:
                print(f"Inserted new ID: {listing_id}")
                total_inserted += 1
                count_in_batch += 1
            else:
                print(f"ID already exists: {listing_id}")

        # Check cap again after each insert
        if TARGET_CAP is not None and total_inserted >= TARGET_CAP:
            break

    # If fewer results returned than maxResults, we're at the end
    if count_in_batch < MAX_RESULTS:
        print("Reached last page of results. Done!")
        break

    # === Update Offset for next page ===
    offset += count_in_batch
    offset_collection.update_one(
        {"_id": "offset_tracker"},
        {"$set": {"last_offset": offset}},
        upsert=True
    )
    print(f"Saved new offset: {offset}")

    # Rate limit
    time.sleep(1)

# === Cleanup ===
client.close()
print("MongoDB connection closed.")
