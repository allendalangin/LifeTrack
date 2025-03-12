import pymongo
from pymongo import MongoClient
from datetime import datetime

import pymongo
from pymongo import MongoClient


MONGO_URI = "mongodb+srv://lodinaval:patrick2@fletapp.g5tl1.mongodb.net/?retryWrites=true&w=majority&appName=FletApp"
client = MongoClient(MONGO_URI)
db = client["LifeTrack"]


"""
# Drop the articles collection if it already exists
if "articles" in db.list_collection_names():
    db.articles.drop()
    print("Dropped existing 'articles' collection.")

# Define the JSON schema for the articles collection
article_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description", "source_name", "date", "image"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "description": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "source_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "date": {
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "image": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "content": {
                "bsonType": "string",
                "description": "optional article content"
            }
        }
    }
}

# Create the articles collection with the specified validator
try:
    db.create_collection("articles", validator=article_validator)
    print("Articles collection created with validation.")
except Exception as e:
    print("Error creating articles collection:", e)

"""

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