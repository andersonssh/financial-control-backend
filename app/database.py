import os
from typing import List

from pymongo import MongoClient

MONGO_USER = os.environ["MONGO_USER"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_DATABASE = os.environ["MONGO_DATABASE"]
MONGO_URL = f"{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE}"
MONGO_OPTIONS = "retryWrites=true&w=majority"

client = MongoClient(f"mongodb+srv://{MONGO_URL}?{MONGO_OPTIONS}")

db = client.get_database(MONGO_DATABASE)


def find(collection: str, filters: dict = None, projection: dict = None) -> List[dict]:
    return list(db.get_collection(collection).find(filters, projection))


def update_one(collection: str, filters: dict, changes: dict) -> bool:
    return bool(db.get_collection(collection).update_one(filters, {"$set": changes}))
