import pymongo
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb+srv://lodinaval:patrick2@fletapp.g5tl1.mongodb.net/?retryWrites=true&w=majority&appName=FletApp"
client = MongoClient(MONGO_URI)
db = client["LifeTrack"]

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["date", "count"],
        "properties": {
            "date": {
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "count": {
                "bsonType": "int",
                "description": "must be a integer and is required"
            },
        }
    }
}

'''
try:
    db.create_collection("vaccination_stats", validator=validator)
    print("Collection 'vaccination stats' created with validation.")
except Exception as e:
    print("Collection might already exist. Updating validator...")
    db.command("collMod", "articles", validator=validator)
    
'''

articles_collection = db["articles"]
resources_collection = db["resources"]
vaccination_stats_collection = db["vaccination_stats"]

sample_data = [
    {"date": datetime(2025, 3, 1), "count": 150},
    {"date": datetime(2025, 3, 2), "count": 200},
    {"date": datetime(2025, 3, 3), "count": 180},
    {"date": datetime(2025, 3, 4), "count": 250},
]

vaccination_stats_collection.insert_many(sample_data)