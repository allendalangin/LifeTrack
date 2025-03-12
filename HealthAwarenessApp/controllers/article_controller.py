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
    date_str = article.published_date
    # Try to parse full ISO datetime first, then fallback to date-only format.
    try:
        if "T" in date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception as e:
        print("Error converting published_date:", date_str, e)
        date_obj = datetime.now()
    
    article_dict = {
        "title": article.title,
        "description": article.description,
        "date": date_obj,  # Stored as a datetime object.
        "content": article.content,
        "source_name": article.source_name,
        "image": article.image,
    }
    result = articles_collection.insert_one(article_dict)
    return str(result.inserted_id)