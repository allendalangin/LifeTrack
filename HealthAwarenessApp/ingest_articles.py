# ingest_articles.py
import json
import urllib.request
from datetime import datetime
from models.article import Article
from controllers.article_controller import create_article

apikey = "5111ef64cdb0c0c8bc6e35bcef2f82e5"
category = "health"
url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=ph&max=10&apikey={apikey}"

def fetch_and_insert_articles():
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data.get("articles", [])
    for art in articles:
        article = Article(
            title=art.get("title", ""),
            description=art.get("description", ""),
            source_name=art.get("source", {}).get("name", "Unknown"),
            published_date=art.get("publishedAt", datetime.now().strftime("%Y-%m-%d")),
            content=art.get("content", ""),
            image=art.get("image", "")
        )
        create_article(article)
        print(f"Inserted article: {article.title}")

if __name__ == "__main__":
    fetch_and_insert_articles()
