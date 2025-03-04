import flet as ft
from flet import Text, Container, SearchBar, border, Column, ListView, alignment, MainAxisAlignment, CrossAxisAlignment, AppBar, PopupMenuItem, PopupMenuButton, ElevatedButton
import requests
from models.article import Article


#ListAppBar
class ArticlesListAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            title = Text("LifeTrack"),
            actions=[
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Dashboard"),
                        PopupMenuItem(text="Health Articles", on_click = lambda _: page.go("/articles")),
                        PopupMenuItem(text="Health Resources", on_click = lambda _: page.go("/resources")),
                        PopupMenuItem(text="Stats", on_click = lambda _: page.go("/stats")),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )
        

# Helper function to fetch articles from the API endpointpy
def fetch_articles():
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

# Convert a dictionary (from API) to an Article model instance
def dict_to_article(article_dict):
    return Article(
        title=article_dict.get("title", ""),
        author=article_dict.get("author", ""),
        published_date=article_dict.get("published_date", ""),
        content=article_dict.get("content", "")
    )

# UI component for a single article
class HealthArticleView(Container):
    def __init__(self, article: Article, page=None):
        super().__init__()
        self.page = page
        self.article = article

    def build_container(self, page=None):
        nav_page = page or self.page
        return Container(
            content=Column(controls=[
                Text(self.article.title, size=18, weight="bold"),
                Text(f"By {self.article.author}", size=16),
                Text(f"Published on: {self.article.published_date}", size=14, weight="italic"),
            ]),
            padding=10,
            border=border.all(1, "white"),
            border_radius=20,
            width=550,
            height=120,
            ink=True,
            on_click=lambda _: (
                setattr(nav_page, "selected_article", self.article), #this is needed to pass the article to article details
                nav_page.go("/article-details"))
        )

def HealthArticlesView(page: ft.Page):
    page.title = "Health Articles"
    page.theme_mode = "dark"
    page.scroll = True
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

    # Function to filter articles based on search query
    def update_list(query):
        filtered = [article for article in articles if query.lower() in article.title.lower()]
        # Rebuild the list view controls
        articles_list.controls = [HealthArticleView(article, page).build_container(page) for article in filtered]
        page.update()

    # Build the search bar
    search_bar = SearchBar(
        bar_hint_text="Search articles...",
        width=600,
        height=50,
        on_change=lambda e: update_list(e.control.value)
    )

    return Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        controls=[
            Container(content=search_bar, margin=20, alignment=ft.alignment.center),
            Container(content=articles_list, height=600, margin=20, alignment=alignment.center),
        ],
        alignment=MainAxisAlignment.CENTER
    )