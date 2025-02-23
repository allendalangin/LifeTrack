import flet as ft

def main(page: ft.Page):
    # Set the page title and window size
    page.title = "Nested Layout Example"
    page.window_width = 1200
    page.window_height = 600

    # Function to create a nested Column layout
    def create_nested_column(header_color, body_color, footer_color):
        return ft.Column(
            controls=[
                ft.Container(
                    expand=1,
                    content=ft.Text("Header", size=20, weight="bold"),
                    bgcolor=header_color,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=1,
                    content=ft.Text("Body", size=20, weight="bold"),
                    bgcolor=body_color,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=1,
                    content=ft.Text("Footer", size=20, weight="bold"),
                    bgcolor=footer_color,
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
        )

    # Create the main Row with three containers
    r = ft.Row(
        controls=[
            ft.Container(
                expand=1,
                content=create_nested_column(
                    ft.colors.BLUE_200, ft.colors.GREEN_200, ft.colors.RED_200
                ),
            ),
            ft.Container(
                expand=1,
                content=create_nested_column(
                    ft.colors.YELLOW_200, ft.colors.PURPLE_200, ft.colors.ORANGE_200
                ),
            ),
            ft.Container(
                expand=1,
                content=create_nested_column(
                    ft.colors.CYAN_200, ft.colors.PINK_200, ft.colors.TEAL_200
                ),
            ),
        ],
        expand=True,
    )

    # Add the layout to the page
    page.add(r)

# Run the app
ft.app(target=main)