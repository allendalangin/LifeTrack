import flet as ft
from flet import *
from flet import Text, Container, SearchBar, border, ElevatedButton, View, IconButton, Icons, AppBar, Row, Icon, ImageFit
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment, PopupMenuButton, PopupMenuItem,Image

class ResourceDetailsAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/resources"),
            ),leading_width=50,
            title = Text("LifeTrack"),
            actions=[
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Dashboard"),
                        PopupMenuItem(text="Health Articles", on_click = lambda _: page.go("/articles")),
                        PopupMenuItem(text="Health Resources", on_click = lambda _: page.go("/resources")),
                        PopupMenuItem(text="Stats"),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )

def ResourceDetailsView(page):
    page.theme_mode = "dark"
    page.title = "Health Resource Details Page"
    resource = getattr(page,"selected_resource", None)
    if not resource:
        return Column(controls=[Text("No selected resource")])
    return Column(
        controls=[
            Text(resource.name, size=24, weight="bold"),
            Image(
                src="/home/ket/LocalRepo/LifeTrack/HealthAwarenessApp/assets/DetailImage",
                width=300,
                height=200,
                fit = ImageFit.CONTAIN
            ),
            Text(
                resource.category, size = 20, italic=True
                ),
            Row(
                controls=[
                    Icon(name=ft.Icons.LOCATION_ON),
                    Text(resource.location)
                ]
                ),
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
        spacing=10
    )