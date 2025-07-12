import requests
import time
import os
import datetime
from dotenv import load_dotenv
from utils.mongo_config import mongo_collection, mongo_client, MONGO_DB_NAME

# Load environment variables
load_dotenv()
DETAILS_COLLECTION_NAME = os.getenv("MONGO_DETAILS_COLLECTION_NAME")
if not DETAILS_COLLECTION_NAME:
    raise ValueError("MONGO_DETAILS_COLLECTION_NAME is not set in .env")

details_collection = mongo_client[MONGO_DB_NAME][DETAILS_COLLECTION_NAME]

# === Phase 1: Read listing IDs from the listing collection ===
ids_cursor = mongo_collection.find({}, {"id": 1})
ids_list = [doc["id"] for doc in ids_cursor]
print(f"Found {len(ids_list)} listing IDs to process.")

# === Phase 2: Loop through each ID and fetch details ===
for listing_id in ids_list:

    # Deduplication check
    existing_count = details_collection.count_documents({
        "$or": [
            {"listingId": listing_id},
            {"listing.id": listing_id}
        ]
    })

    if existing_count > 0:
        print(f"Skipping existing ID: {listing_id}")
        continue

    detail_url = "https://www.cargurus.com/Cars/detailListingJson.action"
    params = {"inventoryListing": listing_id}

    try:
        response = requests.get(detail_url, params=params, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            print(f"Error fetching details for ID {listing_id}: Status {response.status_code}")
            continue

        detail_data = response.json()
        detail_data["listingId"] = listing_id  # Always ensure top-level listingId

        # === Trim the "listing" part only ===
        listing = detail_data.get("listing", {})
        trimmed_listing = {
            "id": listing.get("id"),
            "inclusionType": listing.get("inclusionType"),
            "status": listing.get("status"),
            "listingTitle": listing.get("listingTitle"),
            "listingTitleOnly": listing.get("listingTitleOnly"),
            "vehicleEntityName": listing.get("vehicleEntityName"),
            "price": listing.get("price"),
            "priceString": listing.get("priceString"),
            "expectedPrice": listing.get("expectedPrice"),
            "dealScore": listing.get("dealScore"),
            "mileage": listing.get("mileage"),
            "mileageString": listing.get("mileageString"),
            "vin": listing.get("vin"),
            "description": listing.get("description"),
            "vehicleCondition": listing.get("vehicleCondition"),
            "unitMileage": listing.get("unitMileage"),
            "stockNumber": listing.get("stockNumber"),
            "dealRatingKey": listing.get("dealRatingKey"),
            "localizedTransmission": listing.get("localizedTransmission"),
            "localizedExteriorColor": listing.get("localizedExteriorColor"),
            "localizedInteriorColor": listing.get("localizedInteriorColor"),
            "localizedFuelEconomy": listing.get("localizedFuelEconomy"),
            "localizedDriveTrain": listing.get("localizedDriveTrain"),
            "localizedEngineDisplayName": listing.get("localizedEngineDisplayName"),
            "localizedFuelType": listing.get("localizedFuelType"),
            "fuelTankCapacity": listing.get("fuelTankCapacity"),
            "distance": listing.get("distance"),
            "rawDistance": listing.get("rawDistance"),
            "roundedDistance": listing.get("roundedDistance"),
            "priceDifferential": listing.get("priceDifferential"),
            "pictures": listing.get("pictures"),
            "spin": listing.get("spin"),
            "listingHistory": listing.get("listingHistory"),
            "vehicleHistory": listing.get("vehicleHistory"),
            "highLeverage": listing.get("highLeverage"),
            "savedCount": listing.get("savedCount"),
            "entityId": listing.get("entityId"),
            "powerTypeKey": listing.get("powerTypeKey"),
            "carId": listing.get("carId"),
            "postalCode": listing.get("postalCode"),
            "ncapSafetyRatings": listing.get("ncapSafetyRatings"),
            "listingCondition": listing.get("listingCondition"),
            "makeName": listing.get("makeName"),
            "modelName": listing.get("modelName"),
            "makeId": listing.get("makeId"),
            "modelId": listing.get("modelId"),
            "year": listing.get("year"),
            "trimName": listing.get("trimName"),
            "bodyTypeGroupId": listing.get("bodyTypeGroupId"),
            "vehicleLeagues": listing.get("vehicleLeagues"),
            "cityFuelEconomy": listing.get("cityFuelEconomy"),
            "combinedFuelEconomy": listing.get("combinedFuelEconomy"),
            "highwayFuelEconomy": listing.get("highwayFuelEconomy"),
            "localizedNumberOfDoors": listing.get("localizedNumberOfDoors"),
            "localizedCombinedFuelEconomy": listing.get("localizedCombinedFuelEconomy"),
        }

        # === Build final document with desired shape ===
        final_document = {
            "listingId": detail_data.get("listingId"),
            "listing": trimmed_listing,
            "autoEntityInfo": detail_data.get("autoEntityInfo"),
            "listingDetailStatsSectionDto": detail_data.get("listingDetailStatsSectionDto"),
            "created_at": datetime.datetime.utcnow()

        }

        # === Insert into MongoDB ===
        
        details_collection.insert_one(final_document)
        print(f"Stored details for ID: {listing_id}")

        # Rate limit
        time.sleep(1)

    except Exception as e:
        print(f"Exception while processing ID {listing_id}: {e}")

# === Cleanup ===
mongo_client.close()
print("MongoDB connection closed.")
