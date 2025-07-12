import requests
import os
import datetime
from dotenv import load_dotenv
from utils.mongo_config import mongo_collection, mongo_client, MONGO_DB_NAME

# === Load .env ===
load_dotenv()

COUNTER_COLLECTION_NAME = os.getenv("MONGO_COUNTER_COLLECTION_NAME")
if not COUNTER_COLLECTION_NAME:
    raise ValueError("MONGO_COUNTER_COLLECTION_NAME is not set in .env")

# Connect to the counter collection
counter_collection = mongo_client[MONGO_DB_NAME][COUNTER_COLLECTION_NAME]

# === Ensure unique index on 'id' ===
mongo_collection.create_index("id", unique=True)

# === Initialize counter document if not exists ===
counter_doc = counter_collection.find_one({})
if counter_doc is None:
    counter_collection.insert_one({"seq": 0, "last_offset": 0})
    print("[Init] Counter collection created with seq = 0 and last_offset = 0")
    counter_doc = {"seq": 0, "last_offset": 0}

# === Config ===
ZIP = "76131"
DISTANCE = 100
MAX_RESULT = 20   # Fetch 20 per page
CAP = 30        # Or set to None for unlimited
new_insert_count = 0 #total new inserts of id

HEADERS = {"User-Agent": "Mozilla/5.0"}

# === Start from last_offset in DB ===
current_offset = counter_doc.get("last_offset", 0)
print(f"[Start] Beginning at offset: {current_offset}")

total_new_inserted = 0

while True:
    if CAP and total_new_inserted >= CAP:
        print(f"[Stop] Reached CAP limit of {CAP}.")
        break

    # Build URL
    params = {
        "zip": ZIP,
        "distance": DISTANCE,
        "maxResults": MAX_RESULT,
        "offset": current_offset
    }

    print(f"[Request] Offset {current_offset}")
    try:
        response = requests.get(
            "https://www.cargurus.com/Cars/searchResults.action",
            params=params,
            headers=HEADERS,
            timeout=10  # Set timeout to 10 seconds
        )

        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
    except requests.exceptions.Timeout:
        print("[Timeout] Server didn't respond in 10 seconds. Skipping...")
        continue
    except requests.exceptions.RequestException as e:
        print(f"[Request Error] {e}. Skipping...")
        continue


      

    data = response.json()

    if not data:
        print("[End] No more results.")
        break

    new_this_page = 0

    for listing in data:
        listing_id = listing.get("id")
        listing_offset = listing.get("offset")
        if listing_id:
            # Try to insert (unique index on 'id')
            result = mongo_collection.update_one(
                {"id": listing_id},
                {
                    "$setOnInsert": {
                        "id": listing_id,
                        "offset": listing_offset,
                        "created_at": datetime.datetime.utcnow()
                    }
                },
                upsert=True
            )

            if result.upserted_id:
                # Increment seq in counter
                updated_counter = counter_collection.find_one_and_update(
                    {},
                    {"$inc": {"seq": 1}},
                    return_document=True
                )
                custom_counter = updated_counter["seq"]

                # Add counter to document
                mongo_collection.update_one(
                    {"id": listing_id},
                    {"$set": {"customCounter": custom_counter}}
                )

                print(f"Inserted NEW ID: {listing_id} with counter {custom_counter}")
                new_this_page += 1
                total_new_inserted += 1
                
                # === Check CAP ===
                if CAP is not None and total_new_inserted >= CAP:
                    print(f"[Stop] Reached CAP limit of {CAP}.")
                    break
            else:
                print(f"ID already exists: {listing_id}")

    # Advance offset
    current_offset += len(data)
    counter_collection.update_one(
        {},
        {"$set": {"last_offset": current_offset}},
        upsert=True
    )
    print(f"[Offset Saved] Now at {current_offset}")

    if len(data) < MAX_RESULT:
        print("[End] Fewer than MAX_RESULT returned—probably last page.")
        break

print(f"[Done] Total new inserted this run: {total_new_inserted}")
mongo_client.close()
