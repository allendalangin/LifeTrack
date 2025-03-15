# src/views/article_details_view.py

import flet as ft
from flet import Text, Container, Column, Image

class DetailsAppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color="#0cb4cc",
                on_click=lambda e: self.handle_back_navigation(page),  # Handle back navigation
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

    def handle_back_navigation(self, page):
        """Navigate back to the correct route based on the source route."""
        source_route = getattr(page, "source_route", "/home")  # Default to /home if source_route is not set
        page.go(source_route)  # Navigate back to the source route

def ArticleDetailsView(page: ft.Page):
    page.title = "Article Details"
    article = getattr(page, "selected_article", None)
    if not article:
        return ft.View(
            "/article-details",
            controls=[Text("No article selected.")],
            appbar=DetailsAppBar(page),  # Add the app bar
        )
    
    return ft.View(
        "/article-details",
        appbar=DetailsAppBar(page),  # Add the app bar
        controls=[
            Column(
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
                controls=[
                    # Big image at the top
                    Image(
                        src=article.image,
                        width=page.window.width,  # Set width to window width
                        height=400,
                        fit=ft.ImageFit.COVER
                    ),
                    Container(
                        content=Text(article.title, size=24, weight="bold"),
                        padding=10,
                        width=page.window.width,  # Set width to window width
                    ),
                    Container(
                        content=Text(f"Description: {article.description}", size=16, italic=True),
                        padding=10,
                        width=page.window.width,  # Set width to window width
                    ),
                    Container(
                        content=Text(f"Publish Date: {article.published_date}", size=12, color=ft.Colors.GREY),
                        padding=10,
                        width=page.window.width,  # Set width to window width
                    ),
                    Container(
                        content=Text(article.content, width=page.window.width),  # Set width to window width
                        padding=10,
                        width=page.window.width,  # Set width to window width
                    )
                ]
            )
        ]
    )