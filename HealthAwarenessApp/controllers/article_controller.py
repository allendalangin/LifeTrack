from datetime import datetime
from models.article import Article
from database import articles_collection

def article_helper(article_doc) -> Article:
    return Article(
        title=article_doc["title"],
        author=article_doc["author"],
        published_date=article_doc["date"].strftime("%Y-%m-%d"),
        content=article_doc.get("content", "")
    )

def get_all_articles():
    articles_cursor = articles_collection.find()
    return [article_helper(doc) for doc in articles_cursor]

def create_article(article: Article):
    article_dict = {
        "title": article.title,
        "author": article.author,
        # Convert the string date to a datetime object
        "date": datetime.strptime(article.published_date, "%Y-%m-%d"),
        "content": article.content,
    }
    result = articles_collection.insert_one(article_dict)
    return str(result.inserted_id)