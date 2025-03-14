# src/views/health_articles_view.py

import flet as ft
from src.models.article_model import Article
from src.controllers.article_controller import ArticleController

class HealthArticlesView(ft.View):
    def __init__(self, page: ft.Page, controller: ArticleController):
        super().__init__()
        self.page = page
        self.controller = controller
        self.page.title = "Health Articles"
        self.page.scroll = True
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Add a loading spinner
        self.loading_ring = ft.ProgressRing(visible=True)
        self.articles_list = ft.ListView(expand=True, spacing=20, width=600)
        self.search_bar = ft.SearchBar(
            bar_hint_text="Search articles...",
            width=600,
            height=50,
            on_change=lambda e: self.update_list(e.control.value)
        )

        self.controls = [
            ft.Container(content=self.search_bar, margin=20, alignment=ft.alignment.center),
            ft.Container(content=self.loading_ring, margin=20, alignment=ft.alignment.center),
            ft.Container(content=self.articles_list, height=600, margin=20, alignment=ft.alignment.center),
        ]

        # Set the custom app bar
        self.appbar = DetailsAppBar(page)

        # Start fetching articles asynchronously
        self.page.run_task(self.fetch_and_display_articles)

    async def fetch_and_display_articles(self):
        """Fetch articles from the API and update the UI."""
        articles = await self.controller.fetch_articles()  # Reuse cached articles
        self.articles_list.controls = [self.build_article_container(article) for article in articles]
        self.loading_ring.visible = False  # Hide the loading spinner
        self.page.update()

    def build_article_container(self, article: Article):
        """Build a container for an article with a hover effect."""
        container = ft.Container(
            bgcolor=ft.colors.WHITE10,
            padding=15,
            border_radius=10,
            width=350,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Image(
                        src=article.image,
                        width=320,
                        height=180,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text(
                        article.title,
                        size=16,
                        weight="bold"
                    ),
                    ft.Text(
                        f"{article.description}",
                        size=14
                    ),
                    ft.Text(
                        "Read More >",
                        weight="bold",
                        color=ft.colors.BLUE
                    ),
                ],
            ),
            scale=ft.transform.Scale(scale=1),  # Initial scale
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),  # Smooth animation
        )

        def on_hover(e):
            """Handle hover events for the container."""
            if e.data == "true":
                # Magnify the container on hover
                container.scale = ft.transform.Scale(scale=1.05)
            else:
                # Reset the container on hover exit
                container.scale = ft.transform.Scale(scale=1)
            container.update()

        return ft.GestureDetector(
            content=container,
            on_tap=lambda _: self.navigate_to_article_details(article),  # Make the container clickable
            on_hover=on_hover,  # Add hover effect
        )

    def navigate_to_article_details(self, article):
        """Navigate to the article details view."""
        setattr(self.page, "selected_article", article)  # Store the selected article
        setattr(self.page, "source_route", "/news")  # Store the source route
        self.page.go("/article-details")  # Navigate to the article details view

    def update_list(self, query):
        """Filter articles based on search query."""
        articles = self.controller.cached_articles  # Use cached articles
        if articles:
            filtered = [article for article in articles if query.lower() in article.title.lower()]
            self.articles_list.controls = [self.build_article_container(article) for article in filtered]
            self.page.update()

class DetailsAppBar(ft.AppBar):
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