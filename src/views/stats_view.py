# src/views/stats_view.py

import flet as ft

# Base64-encoded white image (1x1 pixel)
WHITE_IMAGE_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAgAB/1h8+AAAAABJRU5ErkJggg=="

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

class StatsView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.filter_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("By Year"),
                ft.dropdown.Option("By Region")
            ],
            value="Select a Category"
        )
        self.data_dropdown = ft.Dropdown()
        self.image = ft.Image(src_base64=WHITE_IMAGE_BASE64)  # Initialize with a blank white image

    def build(self):
        async def update_data_dropdown(e):
            if self.filter_dropdown.value == "By Year":
                data_options = await self.controller.model.fetch_data("by_year")
            elif self.filter_dropdown.value == "By Region":
                data_options = await self.controller.model.fetch_data("by_region")

            else:
                data_options = []
            
            
            # Update dropdown options
            self.data_dropdown.options = [ft.dropdown.Option(d["table_title"]) for d in data_options]
            self.data_dropdown.update()  # Update the dropdown UI
            self.page.update()  # Force a UI refresh

            # Reset the image
            self.image.src_base64 = WHITE_IMAGE_BASE64
            self.image.update()

        async def update_chart(e):
            if self.filter_dropdown.value == "By Year":
                data_options = await self.controller.model.fetch_data("by_year")
            elif self.filter_dropdown.value == "By Region":
                data_options = await self.controller.model.fetch_data("by_region")
            else:
                data_options = []
            
            if self.data_dropdown.value:
                selected_data = next((d for d in data_options if d["table_title"] == self.data_dropdown.value), None)
                if selected_data:
                    img_data = await self.controller.plot_data(selected_data)
                    self.image.src_base64 = img_data
                    self.image.update()

        self.filter_dropdown.on_change = update_data_dropdown
        self.data_dropdown.on_change = update_chart

        # Create the AppBar
        appbar = DetailsAppBar(self.page)

        # Create a Row for the dropdowns with expand=1 and expand=3
        dropdown_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("Select a Category", size=18, weight="bold"),
                        self.filter_dropdown
                    ]),
                    expand=1,  # 25% of the available space
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Select Data to Display", size=18, weight="bold"),
                        self.data_dropdown
                    ]),
                    expand=3,  # 75% of the available space
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        return ft.View(
            "/stats",
            appbar=appbar,
            controls=[
                ft.Column(
                    controls=[
                        dropdown_row,  # Row with dropdowns (stays at the top)
                        ft.Container(
                            content=self.image,  # Image or blank white image
                            expand=True,  # Allow the image to expand
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,  # Align dropdowns at the top
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,  # Allow the column to take up available space
                )
            ]
        )