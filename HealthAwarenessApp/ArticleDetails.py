import flet as ft
from flet import *
from flet import Text, Container, SearchBar, border, ElevatedButton, View, IconButton, Icons
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment, PopupMenuItem

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

def ArticleDetailsView(page):
    page.theme_mode = "dark"
    page.title = "Health Article Details Page"
    return Column(
        controls=[
            Text("The Benefits of a Balanced Diet", size=24, weight="bold"),
            Image(
                src="/home/ket/LocalRepo/LifeTrack/HealthAwarenessApp/assets/DetailImage",
                width=300,
                height=200,
                fit = ImageFit.CONTAIN
            ),
            Text(
                "Author: Dr. Smith",
                size=16,
                italic = True,
            ),
            Text(
                "Publish Date: 02-20-2025",
                size = 12,
                color = ft.Colors.GREY
            ),
            Text(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
                width=700,
                height=100,
            ),
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
        spacing=10
    )

    
    
                    


if __name__ == "__main__":
    ft.app(main)