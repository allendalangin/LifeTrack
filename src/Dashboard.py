import flet as ft

# Function to navigate to different sections
def show_dashboard(page):
    page.clean()  # Clear previous content
    page.title = "Dashboard"

    # Function to create clickable containers for navigation
    def create_clickable_container(label, bgcolor, width, height, destination):
        return ft.Container(
            content=ft.Text(label),
            bgcolor=bgcolor,
            height=height,
            width=width,
            padding=10,
            border_radius=10,
            on_click=lambda e: destination(page)  # Navigate on click
        )

    # Containers as navigation links
    top_container = ft.Container(
        content=ft.Text("Hello, User"),
        bgcolor=ft.colors.RED_100,
        height=232,
        width=610,
        padding=10,
        border_radius=10
    )

    middle_left_container = create_clickable_container("Vaccination Schedule", ft.colors.YELLOW_200, 282, 232, show_vaccination_schedule)
    middle_right_container = create_clickable_container("Health Resources", ft.colors.BLUE_200, 282, 232, show_health_resources)

    # Middle section with two columns
    middle_container = ft.Container(
        content=ft.Row(
            controls=[middle_left_container, middle_right_container],
            spacing=10  # Small gap between sections
        ),
        height=210,
        width=610
    )

    bottom_container = create_clickable_container("Stats", ft.colors.PURPLE_100, 610, 232, show_stats)

    # Left side container
    left_container = ft.Container(
        content=ft.Column(
            controls=[top_container, middle_container, bottom_container],
        ),
        expand=3,
        margin=ft.margin.only(right=5),
        alignment=ft.alignment.center_right
    )

    # Right container (News Articles)
    right_container = create_clickable_container("News Articles", ft.colors.GREEN_100, 300, 1000, show_news_articles)
    
    # Layout
    layout = ft.Row(
        controls=[left_container, right_container],
        expand=True
    )

    page.add(layout)
    page.update()

# Function for the Vaccination Schedule page
def show_vaccination_schedule(page):
    page.clean()
    page.title = "Vaccination Schedule"
    page.add(
        ft.Text("Vaccination Schedule Page"),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: show_dashboard(page))
    )
    page.update()

# Function for the Health Resources page
def show_health_resources(page):
    page.clean()
    page.title = "Health Resources"
    page.add(
        ft.Text("Health Resources Page"),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: show_dashboard(page))
    )
    page.update()

# Function for the Stats page
def show_stats(page):
    page.clean()
    page.title = "Stats"
    page.add(
        ft.Text("Stats Page"),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: show_dashboard(page))
    )
    page.update()

# Function for the News Articles page
def show_news_articles(page):
    page.clean()
    page.title = "News Articles"
    page.add(
        ft.Text("News Articles Page"),
        ft.ElevatedButton("Back to Dashboard", on_click=lambda e: show_dashboard(page))
    )
    page.update()

# Main function to start the app
def main(page: ft.Page):
    show_dashboard(page)

# Run the app in Ubuntu VS Code Terminal
ft.app(target=main)