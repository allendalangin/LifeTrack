import flet as ft
from flet import *
from flet import Text, Container, SearchBar, border, ElevatedButton, View, IconButton, Icons
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment

class ResourceDetailsAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/resources"),
            ),leading_width=50,
        )

def ResourceDetailsView(page):
    page.theme_mode = "dark"
    page.title = "Health Resource Details Page"
    return Column(
        controls=[
            Text("St. Luke's Medical Center", size=24, weight="bold"),
            Image(
                src="/home/ket/LocalRepo/LifeTrack/HealthAwarenessApp/assets/DetailImage",
                width=300,
                height=200,
                fit = ImageFit.CONTAIN
            ),
            Text(
                "St. Luke's Medical Center is one of the leading hospitals in Quezon City, known for its state-of-the-art facilities and compassionate care.",
                size=16,
            ),
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
        spacing=10
    )

    
    
                    


if __name__ == "__main__":
    ft.app(main)