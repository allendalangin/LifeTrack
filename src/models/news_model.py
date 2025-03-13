# src/models/news_model.py

import requests
import asyncio

class NewsModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.news_articles = []  # Cache for news articles

    async def fetch_news_articles(self):
        """Fetch news articles from NewsAPI asynchronously."""
        url = f"https://newsapi.org/v2/everything?q=health&apiKey={self.api_key}"
        try:
            response = await asyncio.to_thread(requests.get, url)  # Run in a separate thread
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            self.news_articles = data.get("articles", [])  # Cache the list of articles
        except Exception as e:
            print(f"Error fetching news: {e}")
            self.news_articles = []  # Return an empty list if there's an error

    def get_news_articles(self):
        """Return the cached news articles."""
        return self.news_articles