# src/controllers/news_controller.py

from src.models.news_model import NewsModel

class NewsController:
    def __init__(self, view, api_key):
        self.view = view  # Initialize the view
        self.model = NewsModel(api_key)

    async def load_news(self):
        """Fetch news articles and update the view."""
        await self.model.fetch_news_articles()
        if self.view:  # Check if view is set
            self.view.update_news(self.model.get_news_articles())