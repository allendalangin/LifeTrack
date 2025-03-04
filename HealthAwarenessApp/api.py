from fastapi import FastAPI, HTTPException
from models.article import Article
from models.resource import Resource
from controllers.article_controller import get_all_articles, create_article
from controllers.resource_controller import get_all_resources, create_resource
from controllers.vaccination_controller import get_vaccination_stats

app = FastAPI()

@app.get("/articles")
def read_articles():
    """Endpoint to retrieve all articles."""
    return get_all_articles()

@app.post("/articles")
def add_article(article: Article):
    """Endpoint to create a new article."""
    try:
        article_id = create_article(article)
        return {"id": article_id, "message": "Article created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resources")
def read_resources():
    """Endpoint to retrieve all articles."""
    return get_all_resources()

@app.post("/resources")
def add_resource(resource: Resource):
    """Endpoint to create a new article."""
    try:
        resource_id = create_resource(resource)
        return {"id": resource_id, "message": "Resource created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/vaccination-stats")
def read_vaccination_stats():
    return get_vaccination_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)