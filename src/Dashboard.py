import flet as ft

# Function to create a container with hover and click functionality
def create_container(text1, bgcolor, page, destination=None, hover_color=None):
    container = ft.Container(
        content=ft.Column(  # Use ft.Column for vertical arrangement
            controls=[
                ft.Text(text1, size=20, weight="bold"),  # First text
                ft.Text("View " + text1, size=16, color=ft.Colors.GREY_600),  # Second text
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center the texts vertically
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center the texts horizontally
        ),
        border_radius=10,
        bgcolor=bgcolor,
        expand=True,
        alignment=ft.alignment.center,
    )

    # Function to handle hover events
    def on_hover(e):
        container.bgcolor = hover_color if e.data == "true" else bgcolor
        container.update()

    # Attach the hover event
    container.on_hover = on_hover

    # Attach the click event if a destination is provided
    if destination:
        container.on_click = lambda e: navigate_to(destination, page)

    return container

def on_logout_click(e, page):
    page.go("/login")

# Central routing function
def navigate_to(destination, page):
    page.clean()  # Clear the current page
    destination(page)  # Call the destination function

# Function to show the Vaccination Schedule page
def show_vaccination_schedule(page):
    page.title = "Vaccination Schedule"
    page.add(
        create_container("Vaccination Schedule Page", ft.Colors.WHITE, page),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: navigate_to(show_dashboard, page))
    )
    page.update()

# Function to show the Health Resources page
def show_health_resources(page):
    page.title = "Health Resources"
    page.add(
        create_container("Health Resources Page", ft.Colors.WHITE, page),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: navigate_to(show_dashboard, page))
    )
    page.update()

# Function to show the Stats page
def show_stats(page):
    page.title = "Stats"
    page.add(
        create_container("Stats Page", ft.Colors.WHITE, page),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: navigate_to(show_dashboard, page))
    )
    page.update()

# Function to show the News Articles page
def show_news_articles(page):
    page.title = "News Articles"
    page.add(
        create_container("News Articles Page", ft.Colors.WHITE, page),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: navigate_to(show_dashboard, page))
    )
    page.update()

# Function to show the Dashboard
def show_dashboard(page):
    page.title = "Dashboard"

    def create_nested_column(header_color, body_color, footer_color):
        return ft.Column(
            controls=[
                ft.Container(
                    expand=3,
                    content=ft.Row(
                        controls=[
                            ft.Text("Hello, User", size=20, weight="bold"),
                            ft.ElevatedButton("Logout", on_click=lambda e: on_logout_click(e, page))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=5,
                    bgcolor=header_color,
                    alignment=ft.alignment.bottom_left,
                ),
                ft.Container(
                    expand=4,
                    content=create_nested_row(ft.Colors.WHITE, page),
                    bgcolor=body_color,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=4,
                    content=create_container("Statistics", footer_color, page, destination=show_stats, hover_color=ft.Colors.RED_100),
                    bgcolor=ft.Colors.WHITE,
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
        )

    def create_nested_row(body_color, page):
        return ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 6},
                    controls=[
                        ft.Container(
                            content=create_container("Vaccination Schedules", ft.Colors.AMBER_300, page, destination=show_vaccination_schedule, hover_color=ft.Colors.AMBER_500),
                            bgcolor=ft.Colors.WHITE,
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ],
                ),
                ft.Column(
                    col={"sm": 12, "md": 6},
                    controls=[
                        ft.Container(
                            content=create_container("Health Resources", ft.Colors.GREEN_300, page, destination=show_health_resources, hover_color=ft.Colors.GREEN_500),
                            bgcolor=ft.Colors.WHITE,
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ],
                ),
            ],
            expand=True,
        )

    # Create the main layout
    main_layout = ft.ResponsiveRow(
        controls=[
            ft.Column(
                col={"sm": 12, "md": 9},
                controls=[
                    create_nested_column(
                        ft.Colors.BLUE_200, ft.Colors.WHITE, ft.Colors.RED_200
                    ),
                ],
                expand=True,
            ),
            ft.Column(
                col={"sm": 12, "md": 3},
                controls=[
                    ft.Container(
                        content=create_container("Articles", ft.Colors.YELLOW_200, page, destination=show_news_articles, hover_color=ft.Colors.YELLOW_500),
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        ],
        adaptive=True,
        expand=True,
    )

    page.add(main_layout)

# Main function to start the app
def main(page: ft.Page):
    page.window.width=1200
    page.window.height=600
    page.update()
    show_dashboard(page)  # Start with the dashboard

ft.app(target=main)