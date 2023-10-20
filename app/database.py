import os
import copy
from typing import List

from pymongo import MongoClient

mongo_host = os.environ["MONGO_HOST"]
mongo_database = os.environ["MONGO_DATABASE"]
if mongo_host == "localhost":
    client = MongoClient()
else:
    mongo_user = os.environ["MONGO_USER"]
    mongo_password = os.environ["MONGO_PASSWORD"]
    mongo_url = f"{mongo_user}:{mongo_password}@{mongo_host}/{mongo_database}"
    mongo_options = "retryWrites=true&w=majority"
    client = MongoClient(f"mongodb+srv://{mongo_url}?{mongo_options}")

db = client.get_database(mongo_database)


def find(collection: str, filters: dict = None, projection: dict = None) -> List[dict]:
    return list(db.get_collection(collection).find(filters, projection))


def insert_one(collection: str, document: dict) -> dict | None:
    inserted_id = db.get_collection(collection).insert_one(document).inserted_id
    if not inserted_id:
        return None
    document = copy.deepcopy(document)
    document["_id"] = inserted_id
    return document


def update_one(
    collection: str, filters: dict, changes: dict, operation: str = "$set"
) -> bool:
    return (
        db.get_collection(collection)
        .update_one(filters, {operation: changes})
        .modified_count
        == 1
    )
