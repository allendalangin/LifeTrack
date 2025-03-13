from pymongo import MongoClient

class StatsModel:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.statistics
        self.by_year_collection = self.db.by_year
        self.by_region_collection = self.db.by_region

    def fetch_data(self, collection_name):
        if collection_name == "by_year":
            return list(self.by_year_collection.find())
        elif collection_name == "by_region":
            return list(self.by_region_collection.find())
        else:
            return []