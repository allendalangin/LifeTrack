from datetime import datetime
from models.resource import Resource
from database import resources_collection

def resource_helper(resource_doc) -> Resource:
    return Resource(
        name=resource_doc["name"],
        category=resource_doc["category"],
        location=resource_doc["location"],
    )

def get_all_resources():
    resources_cursor = resources_collection.find()
    return [resource_helper(doc) for doc in resources_cursor]

def create_resource(resource: Resource):
    resource_dict = {
        "name" : resource.name,
        "category" : resource.category,
        "location" : resource.location,
    }
    result = resources_collection.insert_one(resource_dict)
    return str(result.inserted_id)