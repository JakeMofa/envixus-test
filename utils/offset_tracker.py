import os
from dotenv import load_dotenv
from utils.mongo_config import mongo_client, MONGO_DB_NAME

# Load .env
load_dotenv()
COUNTER_COLLECTION_NAME = os.getenv("MONGO_COUNTER_COLLECTION_NAME")
if not COUNTER_COLLECTION_NAME:
    raise ValueError("MONGO_COUNTER_COLLECTION_NAME is not set in .env")

counter_collection = mongo_client[MONGO_DB_NAME][COUNTER_COLLECTION_NAME]

result = counter_collection.update_one({}, {"$set": {"seq": 0}})
print("[Done] Counter (seq) reset to 0.")

mongo_client.close()
