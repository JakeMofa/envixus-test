import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection info from .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Validate required variables
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in .env file")
if not MONGO_DB_NAME:
    raise ValueError("MONGO_DB_NAME is not set in .env file")
if not MONGO_COLLECTION_NAME:
    raise ValueError("MONGO_COLLECTION_NAME is not set in .env file")

# Connect to MongoDB
try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB_NAME]
    mongo_collection = mongo_db[MONGO_COLLECTION_NAME]
    print(f" Connected to MongoDB at {MONGO_URI}, using database '{MONGO_DB_NAME}' and collection '{MONGO_COLLECTION_NAME}'")
except Exception as e:
    print(" Error connecting to MongoDB:", e)
