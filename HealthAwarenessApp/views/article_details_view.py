import flet as ft
from flet import Text, Container, ElevatedButton, IconButton, PopupMenuItem, Image
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, AppBar, PopupMenuButton

class ArticleDetailsAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            leading=IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/articles"),
            ),
            leading_width=50,
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

def ArticleDetailsView(page: ft.Page):
    page.title = "Article Details"
    article = getattr(page, "selected_article", None)
    if not article:
        return Column(controls=[Text("No article selected.")])
    return Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        controls=[
            # Big image at the top
            Image(
                src=article.image,
                width=600,
                height=400,
                fit=ft.ImageFit.COVER
            ),
            Text(article.title, size=24, weight="bold"),
            Text(f"Description: {article.description}", size=16, italic=True),
            Text(f"Publish Date: {article.published_date}", size=12, color=ft.Colors.GREY),
            Container(
                content=Text(article.content, width=700),
                padding=10
            )
        ]
    )
