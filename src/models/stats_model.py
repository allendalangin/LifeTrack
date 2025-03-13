# src/models/stats_model.py

import httpx

class StatsModel:
    def __init__(self, api_url):
        self.api_url = api_url

    async def fetch_data(self, collection_name):
        """
        Fetch statistics data from the FastAPI backend.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/stats/{collection_name}")
            if response.status_code == 200:
                return response.json()
            else:
                return []