from datetime import datetime
from models.article import Article
from database import articles_collection

def article_helper(article_doc) -> Article:
    return Article(
        title=article_doc["title"],
        description=article_doc["description"],
        source_name=article_doc["source_name"],
        published_date=article_doc["date"],
        content=article_doc.get("content", ""),
        image=article_doc["image"],
    )

def get_all_articles():
    articles_cursor = articles_collection.find()
    return [article_helper(doc) for doc in articles_cursor]

def create_article(article: Article):
    article_dict = {
        "title": article.title,
        "description": article.description,
        "date": article.published_date,
        "content": article.content,
        "source_name" : article.source_name,
        "image": article.image,
    }
    result = articles_collection.insert_one(article_dict)
    return str(result.inserted_id)