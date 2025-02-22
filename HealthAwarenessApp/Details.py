import flet as ft
from flet import Text, Container, SearchBar, border, ElevatedButton, View, IconButton, Icons
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment

def DetailsView(page):
    page.theme_mode = "dark"
    page.title = "Details Page"
    return Column(
        controls=[
            IconButton(
                icon=ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                on_click = lambda _: page.go("/"),
                )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=MainAxisAlignment.CENTER,
    )
                    


if __name__ == "__main__":
    ft.app(main)