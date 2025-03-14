# src/controllers/article_controller.py

from src.models.article_model import Article

class ArticleController:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.view = None  # Reference to the view for updating the UI
        self.cached_articles = None  # Cache for fetched articles

    async def fetch_articles(self):
        """Fetch articles from the GNews API and cache them."""
        if self.cached_articles is None:  # Only fetch if not already cached
            self.cached_articles = Article.fetch_articles(self.api_key)
        return self.cached_articles

    async def load_news(self):
        """Fetch news articles and update the view."""
        articles = await self.fetch_articles()
        if self.view:  # Check if view is set
            self.view.update_news(articles)  # Update the view with fetched articles