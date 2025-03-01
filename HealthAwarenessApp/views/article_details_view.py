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
                        PopupMenuItem(text="Health Articles"),
                        PopupMenuItem(text="Health Resources"),
                        PopupMenuItem(text="Stats"),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )

def ArticleDetailsView(page: ft.Page):
    page.title = "Article Details"
    return Column(
        controls=[
            Text("The Benefits of a Balanced Diet", size=24, weight="bold"),
            Image(
                src="/path/to/your/image.png",
                width=300,
                height=200,
                fit=ft.ImageFit.CONTAIN
            ),
            Text("Author: Dr. Smith", size=16, italic=True),
            Text("Publish Date: 2025-02-15", size=12, color=ft.Colors.GREY),
            Text("Full article content goes here...", width=700, height=100),
        ]
    )