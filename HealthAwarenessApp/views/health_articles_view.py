import flet as ft
from flet import (
    Text, Container, SearchBar, border, Column, ListView, alignment,
    MainAxisAlignment, CrossAxisAlignment, AppBar, PopupMenuItem,
    PopupMenuButton, ElevatedButton, Image, colors
)
import requests
from models.article import Article


class ArticlesListAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            title=Text("LifeTrack"),
            actions=[
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Dashboard"),
                        PopupMenuItem(text="Health Articles", on_click=lambda _: page.go("/articles")),
                        PopupMenuItem(text="Health Resources", on_click=lambda _: page.go("/resources")),
                        PopupMenuItem(text="Stats", on_click=lambda _: page.go("/stats")),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )

def fetch_articles():
    """Helper function to fetch articles from the API endpoint."""
    try:
        response = requests.get("http://127.0.0.1:8000/articles")
        if response.status_code == 200:
            return response.json()  # Expecting a list of article dictionaries
        else:
            print("Server returned status code", response.status_code)
            return []
    except Exception as e:
        print("Error fetching articles:", e)
        return []

def dict_to_article(article_dict):
    """Convert a dictionary (from API) to an Article model instance."""
    return Article(
        title=article_dict.get("title", ""),
        description=article_dict.get("description", ""),
        published_date=article_dict.get("published_date", ""),
        content=article_dict.get("content", ""),
        source_name=article_dict.get("source_name", ""),
        image=article_dict.get("image", ""),
    )

class HealthArticleView(Container):
    def __init__(self, article: Article, page=None):
        super().__init__()
        self.page = page
        self.article = article

    def build_container(self, page=None):
        nav_page = page or self.page
        return Container(
            # A subtle background color for dark theme; adjust as you like
            bgcolor=colors.WHITE10,
            padding=15,
            border_radius=10,
            width=350,   # Tweak width to your preference
            # Remove height so the container grows with content
            content=Column(
                spacing=8,  # Space between elements
                controls=[
                    Image(
                        src=self.article.image,
                        width=320,
                        height=180,
                        fit=ft.ImageFit.COVER
                    ),
                    Text(
                        self.article.title,
                        size=16,
                        weight="bold"
                    ),
                    # Short description
                    Text(
                        f"{self.article.description}",
                        size=14
                    ),
                    # "Read More" link
                    Text(
                        "Read More >",
                        weight="bold",
                        color=colors.BLUE
                    ),
                ],
            ),
            ink=True,
            on_click=lambda _: (
                setattr(nav_page, "selected_article", self.article),  # pass the article to details
                nav_page.go("/article-details")
            ),
        )

def HealthArticlesView(page: ft.Page):
    page.title = "Health Articles"
    page.theme_mode = "dark"
    page.scroll = True
    # You can remove these if you don't want everything centered
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Fetch articles from the FastAPI backend
    articles_data = fetch_articles()
    articles = [dict_to_article(ad) for ad in articles_data]

    articles_list = ListView(
        expand=True,
        spacing=20,
        width=600,
        controls=[HealthArticleView(article, page).build_container(page) for article in articles]
    )

    def update_list(query):
        """Filter articles based on search query."""
        filtered = [article for article in articles if query.lower() in article.title.lower()]
        articles_list.controls = [HealthArticleView(article, page).build_container(page) for article in filtered]
        page.update()

    search_bar = SearchBar(
        bar_hint_text="Search articles...",
        width=600,
        height=50,
        on_change=lambda e: update_list(e.control.value)
    )

    return Column(
        expand=True,
        controls=[
            Container(content=search_bar, margin=20, alignment=ft.alignment.center),
            Container(content=articles_list, height=600, margin=20, alignment=alignment.center),
        ],
        alignment=MainAxisAlignment.CENTER
    )
