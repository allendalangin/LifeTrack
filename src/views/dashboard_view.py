# src/views/dashboard_view.py

import flet as ft

class DashboardView:
    def __init__(self, page, controller, username=None, news_controller=None):
        self.page = page
        self.controller = controller
        self.username = username
        self.news_controller = news_controller  # Add NewsController
        if self.news_controller:
            self.news_controller.view = self  # Set the view reference in the controller

    def build(self):
        """Build and return the dashboard view."""
        print("Dashboard Loaded")

        # Nested row before usage
        def create_nested_row(body_color, page):
            return ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        col={"sm": 12, "md": 6},
                        controls=[
                            ft.Container(
                                content=self.create_container("Vaccination Schedules", ft.colors.AMBER_300, page, destination="/vaccination", hover_color=ft.colors.AMBER_500),
                                alignment=ft.alignment.center,
                                expand=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        col={"sm": 12, "md": 6},
                        controls=[
                            ft.Container(
                                content=self.create_container("Health Resources", ft.colors.GREEN_300, page, destination="/health", hover_color=ft.colors.GREEN_500),
                                alignment=ft.alignment.center,
                                expand=True,
                            ),
                        ],
                    ),
                ],
                expand=True,
            )

        # Nested column
        def create_nested_column(header_color, body_color, footer_color):
            return ft.Column(
                controls=[
                    ft.Container(
                        expand=3,
                        content=ft.Row(
                            controls=[
                                ft.Text(f"Hello, {self.username if self.username else 'User'}", size=20, weight="bold"),  # Display the username
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=5,
                        bgcolor="#b4e8f0",
                        alignment=ft.alignment.bottom_left,
                    ),
                    ft.Container(
                        expand=4,
                        content=create_nested_row(None, self.page),
                        bgcolor=body_color,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        expand=4,
                        content=self.create_container("Statistics", footer_color, self.page, destination="/stats", hover_color=ft.colors.RED_100),
                        alignment=ft.alignment.center,
                    ),
                ],
                expand=True,
            )

        # Create the "Articles" section
        self.articles_section = ft.Column(
            controls=[
                ft.Text("Latest News", size=18, weight="bold"),  # Title
                ft.ListView(
                    controls=[],  # Initially empty, will be populated by the NewsController
                    expand=True,  # Make the ListView expand to fill available space
                    spacing=10,
                ),
                ft.ElevatedButton(
                    text="See more news",
                    on_click=lambda e: self.page.go("/news"),  # Navigate to /news
                ),
            ],
            expand=True,  # Make the Column expand to fill available space
            spacing=10,
        )

        main_layout = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 9},
                    controls=[create_nested_column(ft.colors.BLUE_200, None, ft.colors.RED_200)],
                    expand=True,
                ),
                ft.Column(
                    col={"sm": 12, "md": 3},
                    controls=[
                        ft.Container(
                            content=self.articles_section,
                            alignment=ft.alignment.center,
                            expand=True,  # Make the Container expand to fill available space
                        ),
                    ],
                    expand=True,
                ),
            ],
            adaptive=True,
            expand=True,
        )

        # Return the dashboard as a view
        return ft.View(
            "/home",
            controls=[main_layout],
            appbar=self.DetailsAppBar(self.page),
            bgcolor="#f2f7ff",
        )

    def update_news(self, news_articles):
        """Update the news articles in the dashboard."""
        self.articles_section.controls[1].controls.clear()  # Clear the ListView
        for article in news_articles[:15]:  # Show first 15 articles
            self.articles_section.controls[1].controls.append(self.create_news_card(article))
        self.page.update()

    # src/views/dashboard_view.py

    def create_news_card(self, article):
        """Create a news card for an article."""
        title = article.title  # Access the title attribute directly
        image_url = article.image  # Access the image attribute directly
        description = article.description  # Access the description attribute directly

        return ft.GestureDetector(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=image_url,
                                width=200,
                                height=100,
                                fit=ft.ImageFit.COVER,
                            ) if image_url else ft.Text("No Image Available"),
                            ft.Text(title, size=14, weight="bold"),
                            ft.Text((description[:100] + "...") if description else "No description available.", size=12),  # Handle empty description
                        ],
                        spacing=5,
                    ),
                    padding=10,
                ),
            ),
            on_tap=lambda e: self.navigate_to_article_details(article),  # Make the card clickable
        )

    def navigate_to_article_details(self, article):
        """Navigate to the article details view."""
        setattr(self.page, "selected_article", article)  # Store the selected article
        setattr(self.page, "source_route", "/home")  # Store the source route
        self.page.go("/article-details")  # Navigate to the article details view

    def navigate_to(self, destination):
        """Navigate to the specified route."""
        self.page.go(destination)

    def create_container(self, text1, bgcolor, page, destination=None, hover_color=None):
        """Create a hoverable container with a click event."""
        container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(text1, size=20, weight="bold"),
                    ft.Text("View " + text1, size=16, color=ft.colors.GREY_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border_radius=10,
            bgcolor=bgcolor,
            expand=True,
            alignment=ft.alignment.center,
            scale=ft.transform.Scale(scale=1),  # Initial scale
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),  # Smooth animation
        )

        def on_hover(e):
            """Handle hover events for the container."""
            if e.data == "true":
                # Magnify the container on hover
                container.scale = ft.transform.Scale(scale=1.034)
                container.bgcolor = hover_color if hover_color else bgcolor
            else:
                # Reset the container on hover exit
                container.scale = ft.transform.Scale(scale=1)
                container.bgcolor = bgcolor
            container.update()

        container.on_hover = on_hover

        if destination:
            container.on_click = lambda e: self.controller.handle_navigation(destination)

        return container

    class DetailsAppBar(ft.AppBar):
        """Custom app bar for the dashboard."""
        def __init__(self, page):
            super().__init__(
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
                actions=[
                    # Wrap PopupMenuButton in a Container to center it vertically
                    ft.Container(
                        content=ft.PopupMenuButton(
                            icon=ft.icons.SETTINGS,
                            icon_color="#0cb4cc",  # Set icon color to #0cb4cc
                            items=[
                                ft.PopupMenuItem(
                                    text="Profile",
                                    on_click=lambda e: print("Profile clicked"),
                                ),
                                ft.PopupMenuItem(
                                    text="Logout",
                                    on_click=lambda e: page.go("/login"),
                                ),
                            ],
                        ),
                        alignment=ft.alignment.center,  # Center the icon vertically
                    ),
                ],
            )

    async def load_news(self):
        """Load news articles asynchronously."""
        if self.news_controller:
            await self.news_controller.load_news()  # Call the correct method