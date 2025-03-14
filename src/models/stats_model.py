# src/models/stats_model.py

import httpx

FASTAPI_URL = "http://127.0.0.1:8000"

class StatsModel:
    async def fetch_data(self, collection_name):
        """
        Fetch statistics data from the FastAPI backend.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FASTAPI_URL}/stats/{collection_name}")
            if response.status_code == 200:
                return response.json()
            else:
                return []