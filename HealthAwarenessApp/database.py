import pymongo
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb+srv://lodinaval:patrick2@fletapp.g5tl1.mongodb.net/?retryWrites=true&w=majority&appName=FletApp"
client = MongoClient(MONGO_URI)
db = client["LifeTrack"]

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "author", "date", "content"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "author": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "date": {
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "content": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }
}

try:
    db.create_collection("articles", validator=validator)
    print("Collection 'articles' created with validation.")
except Exception as e:
    print("Collection might already exist. Updating validator...")
    db.command("collMod", "articles", validator=validator)

articles_collection = db["articles"]
resources_collection = db["resources"]