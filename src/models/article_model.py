# src/models/article_model.py

from dataclasses import dataclass
import json
import urllib.request
from datetime import datetime

@dataclass
class Article:
    title: str
    description: str
    source_name: str
    published_date: str
    image: str
    content: str = ""

    @staticmethod
    def fetch_articles(api_key: str):
        """Fetch articles directly from the GNews API."""
        url = f"https://gnews.io/api/v4/top-headlines?category=health&lang=en&country=ph&max=100&expand=content&apikey={api_key}"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
                articles = data.get("articles", [])
            
            fetched_articles = []
            for art in articles:
                try:
                    published_date = datetime.strptime(
                        art.get("publishedAt", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                except Exception as e:
                    print("Error parsing date for article:", art.get("title", "No Title"), e)
                    published_date = datetime.now()  # Fallback
                
                article = Article(
                    title=art.get("title", ""),
                    description=art.get("description", ""),
                    source_name=art.get("source", {}).get("name", "Unknown"),
                    published_date=published_date.strftime("%Y-%m-%d"),
                    content=art.get("content", ""),
                    image=art.get("image", "")
                )
                fetched_articles.append(article)
            
            return fetched_articles
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")  # Debugging: Print HTTP error details
            return []
        except Exception as e:
            print("Error fetching articles from API:", e)
            return []