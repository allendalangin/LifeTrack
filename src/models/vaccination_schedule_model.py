from pymongo import MongoClient
from pymongo.errors import PyMongoError

class VaccinationScheduleModel:
    def __init__(self, db_name="vaccination", collection_name="vaccination_schedules"):
        self.client = MongoClient("mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_schedules(self):
        """Fetch all vaccination schedules from MongoDB."""
        try:
            schedules = list(self.collection.find({}, {"_id": 0}))  # Exclude _id field
            if not schedules:
                print("No vaccination schedules found in the database.")
                return []
            return schedules
        except PyMongoError as e:
            print(f"Error fetching vaccination schedules: {e}")
            return []