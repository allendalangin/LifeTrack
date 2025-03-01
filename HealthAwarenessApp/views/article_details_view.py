import flet as ft
from flet import Text, Container, SearchBar, border, ElevatedButton, View, IconButton, Icons, PopupMenuItem, Image
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment,AppBar,PopupMenuButton

class ArticleDetailsAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/articles"),
            ),leading_width=50,
            title = Text("LifeTrack"),
            actions=[
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Dashboard"),
                        PopupMenuItem(text="Health Articles", on_click=lambda _: page.go("/articles")),
                        PopupMenuItem(text="Health Resources", on_click=lambda _: page.go("/resources")),
                        PopupMenuItem(text="Stats"),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )

def ArticleDetailsView(page: ft.Page):
    page.title = "Article Details"
    article = getattr(page, "selected_article", None)
    if not article:
        return Column(controls=[Text("No article selected.")])
    return Column(
        controls=[
            Text(article.title, size=24, weight="bold"),
            Image(
                src="/path/to/your/image.png",
                width=300,
                height=200,
                fit=ft.ImageFit.CONTAIN
            ),
            Text(f"By {article.author}", size=16, italic=True),
            Text(f"Publish Date: {article.published_date}", size=12, color=ft.Colors.GREY),
            Text(article.content, width=700, height=100),
        ]
    )