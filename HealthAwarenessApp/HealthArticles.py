import flet as ft
from flet import Text, Container, SearchBar, border
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment

class HealthArticle(Container):
    def __init__(self, title: str, author: str, published_date: str, page=None) -> None:
        super().__init__()
        self.page = page
        self.title = title
        self.author = author
        self.published_date = published_date

    def build_container(self, page=None):
        # Use the page passed to build_container or fallback to self.page
        nav_page = page or self.page
        return Container(
            content=Column(controls=[
                Text(self.title, size=18, weight="bold"),
                Text(f"By {self.author}", size=16),
                Text(f"Published on: {self.published_date}", size=14, weight="italic"),
            ]),
            padding=10,
            border=border.all(1, "white"),
            border_radius=20,
            width=550,
            height=120,
            ink=True,
            on_click=lambda _: nav_page.go("/article-details") if nav_page else None
        )

    @classmethod
    def build_list(cls, articles, page):
        list_view = ListView(
            expand=True,
            spacing=20,
            width=600,
        )
        for article in articles:
            list_view.controls.append(article.build_container(page))
        return list_view

def HealthArticlesView(page: Page):
    page.title = "Health Articles"
    page.theme_mode = "dark"
    page.scroll = True
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    
    # Function to filter articles by title
    def filter_articles(query):
        return [article for article in articles if query.lower() in article.title.lower()]

    # Update list based on the search query
    def update_list(query):
        filtered_articles = filter_articles(query)
        articles_list.controls = [article.build_container(page) for article in filtered_articles]
        page.update()

    # Sample data for health articles (could be fetched via FastAPI)
    articles = [
        HealthArticle("The Benefits of a Balanced Diet", "Dr. Smith", "2025-02-15"),
        HealthArticle("Understanding Heart Health", "Dr. Lee", "2025-01-20"),
        HealthArticle("Mental Health: Breaking the Stigma", "Dr. Jones", "2025-03-01"),
        HealthArticle("Advancements in Telemedicine", "Dr. Patel", "2025-02-28"),
    ]

    # Build the search bar and list of articles
    search_bar = SearchBar(
        bar_hint_text="Search articles...",
        width=600,
        height=50,
        on_change=lambda e: update_list(e.control.value)
    )

    articles_list = HealthArticle.build_list(articles, page)

    return Column(
        controls=[
            Container(content=search_bar, margin=20, alignment=ft.alignment.center),
            Container(content=articles_list, height=600, margin=20, alignment=alignment.center),
        ],
        alignment=MainAxisAlignment.CENTER
    )

if __name__ == "__main__":
    ft.app(target=HealthArticlesView)