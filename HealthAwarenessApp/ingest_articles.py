# ingest_articles.py
import json
import urllib.request
from datetime import datetime
from models.article import Article
from controllers.article_controller import create_article

apikey = "5111ef64cdb0c0c8bc6e35bcef2f82e5"
category = "health"
url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=ph&max=10&expand=content&apikey={apikey}"

def fetch_and_insert_articles():
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data.get("articles", [])
    
    for art in articles:
        # Convert published date string to datetime object. Adjust the format as needed.
        try:
            published_date = datetime.strptime(art.get("publishedAt", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")), "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            print("Error parsing date for article:", art.get("title", "No Title"), e)
            published_date = datetime.now()  # Fallback
        
        article = Article(
            title=art.get("title", ""),
            description=art.get("description", ""),
            source_name=art.get("source", {}).get("name", "Unknown"),
            published_date=published_date.strftime("%Y-%m-%d"),  # Or store the date as a datetime object if your controller expects that.
            content=art.get("content", ""),
            image=art.get("image", "")
        )
        try:
            inserted_id = create_article(article)
            print(f"Inserted article: {article.title} with id {inserted_id}")
        except Exception as e:
            print("Failed to insert article:", article.title, e)

if __name__ == "__main__":
    fetch_and_insert_articles()
