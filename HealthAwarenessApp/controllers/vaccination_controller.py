from datetime import datetime
from database import vaccination_stats_collection

def get_vaccination_stats():
    """
    Retrieve all vaccination stats from MongoDB.
    Returns a list of dicts: [{"date": "YYYY-MM-DD", "count": <int>}, ...]
    """
    docs = vaccination_stats_collection.find().sort("date", 1)
    stats = []
    for doc in docs:
        # Convert date to string for JSON
        stats.append({
            "date": doc["date"].strftime("%Y-%m-%d"),
            "count": doc["count"]
        })
    return stats
