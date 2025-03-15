# src/views/infographics_view.py
import flet as ft
from src.controllers.infographics_controller import InfographicsController

class InfographicsView:
    def __init__(self, page):
        self.page = page
        self.controller = InfographicsController(self)
        self.infographics_grid = ft.GridView(
            expand=True,
            runs_count=3,  # Number of columns
            max_extent=200,  # Width of each grid item
            spacing=10,
            run_spacing=10,
        )

    def update_infographics(self, infographics):
        """Update the grid with infographics."""
        self.infographics_grid.controls.clear()
        for infographic in infographics:
            self.infographics_grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src=infographic["url"],
                                width=150,
                                height=150,
                                fit="contain",
                            ),
                            ft.Text(infographic["public_id"], size=12, text_align="center"),
                        ],
                        alignment="center",
                        spacing=5,
                    ),
                    on_click=lambda e, url=infographic["url"]: self.show_full_image(url),
                )
            )
        self.page.update()

    def show_full_image(self, image_url):
        """Navigate to the full image view."""
        self.page.views.append(
            ft.View(
                "/full_image",
                [
                    SimpleAppBar(self.page),  # Use SimpleAppBar for the full image view
                    ft.ListView(
                        expand=True,
                        controls=[
                            ft.Image(
                                src=image_url,
                                fit="contain",
                                width=self.page.width,
                                height=self.page.height,
                            )
                        ],
                    ),
                ],
            )
        )
        self.page.update()

    def build(self):
        """Build and return the infographics view."""
        self.page.run_task(self.controller.load_infographics)  # Await the coroutine
        return ft.View(
            "/infographics",
            [
                DetailsAppBar(self.page),  # Use DetailsAppBar for the infographics view
                self.infographics_grid,
            ],
        )

class DetailsAppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color="#0cb4cc",
                on_click=lambda e: page.go("/home"),
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

class SimpleAppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color="#0cb4cc",
                on_click=lambda e: self.go_back(page),
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

    def go_back(self, page):
        """Navigate back to the previous page."""
        if len(page.views) > 1:
            page.views.pop()  # Remove the current view
            top_view = page.views[-1]  # Get the previous view
            page.go(top_view.route)  # Navigate to the previous route