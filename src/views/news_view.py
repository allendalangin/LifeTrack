# src/views/news_view.py

import flet as ft

class NewsView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.news_articles = []

    def build(self):
        """Build and return the news view."""
        self.news_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
        )

        return ft.View(
            "/news",
            controls=[
                self.NewsAppBar(self.page),
                ft.Text("Latest News", size=24, weight="bold"),
                ft.Container(
                    content=self.news_list,
                    expand=True,
                ),
            ],
            padding=0,
            spacing=0,
        )

    def update_news(self, news_articles):
        """Update the news articles in the view."""
        self.news_articles = news_articles
        self.news_list.controls.clear()
        for article in news_articles:
            self.news_list.controls.append(self.create_news_card(article))
        self.page.update()

    def create_news_card(self, article):
        """Create a news card for an article."""
        title = article.get("title", "No Title")
        image_url = article.get("urlToImage", "")
        description = article.get("description", "")  # Default to empty string if description is None

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Image(
                            src=image_url,
                            width=200,
                            height=100,
                            fit=ft.ImageFit.COVER,
                        ) if image_url else ft.Text("No Image Available"),
                        ft.Text(title, size=14, weight="bold"),
                        ft.Text((description[:100] + "...") if description else "No description available.", size=12),  # Handle None description
                    ],
                    spacing=5,
                ),
                padding=10,
            ),
        )

    class NewsAppBar(ft.AppBar):
        def __init__(self, page):
            super().__init__(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#0cb4cc",
                    on_click=lambda e: page.go("/home"),
                ),
                title=ft.Column(
                    controls=[
                        ft.Container(height=3),
                        ft.Image(
                            src="src/assets/LifeTrackLogo.png",
                            height=55,
                            fit=ft.ImageFit.FIT_HEIGHT,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                center_title=True,
                toolbar_height=50,
            )