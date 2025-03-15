<<<<<<< HEAD
from pymongo import MongoClient

class VaccinationScheduleModel:
    def __init__(self, db_name="vaccination_db", collection_name="vaccination_schedules"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_schedules(self):
        """Fetch all vaccination schedules from MongoDB."""
        schedules = list(self.collection.find({}, {"_id": 0}))  # Exclude _id field
        return schedules if schedules else []
=======
class Vaccination:
    month : str
    hospital : str
    location : str
    date : str
    time : str
    vaccine : str
    
>>>>>>> b68276fb17266da6ae1e5f546f4c353f6d64abc8
