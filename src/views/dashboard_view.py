import flet as ft

# src/views/dashboard_view.py

import flet as ft

class DashboardView:
    def __init__(self, page, controller, news_controller=None):
        self.page = page
        self.controller = controller
        self.username = page.username  # Fetch username from the page object
        self.news_controller = news_controller
        if self.news_controller:
            self.news_controller.view = self

        # Add attributes for weather data containers
        self.air_quality_container = None
        self.temperature_container = None
        self.humidity_container = None
        self.uv_index_container = None
        self.wind_speed_container = None

    def categorize_aqi(self, aqi):
        """Categorize the Air Quality Index (AQI)."""
        if aqi <= 50:
            return "Good"
        elif 51 <= aqi <= 100:
            return "Moderate"
        elif 101 <= aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif 151 <= aqi <= 200:
            return "Unhealthy"
        elif 201 <= aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    def categorize_temp(self, temp):
        """Categorize the temperature."""
        if temp < 10:
            return "Cold"
        elif 10 <= temp < 20:
            return "Cool"
        elif 20 <= temp < 30:
            return "Warm"
        else:
            return "Hot"

    def categorize_humidity(self, humidity):
        """Categorize the humidity."""
        if humidity < 30:
            return "Dry"
        elif 30 <= humidity < 60:
            return "Comfortable"
        else:
            return "Humid"

    def categorize_uv_index(self, uvi):
        """Categorize the UV Index."""
        if uvi <= 2:
            return "Low (green)"
        elif 3 <= uvi <= 5:
            return "Moderate (yellow)"
        elif 6 <= uvi <= 7:
            return "High (orange)"
        elif 8 <= uvi <= 10:
            return "Very High (red)"
        else:
            return "Extreme (violet)"

    def categorize_wind_speed(self, wind_speed):
        """Categorize the wind speed."""
        if wind_speed < 1:
            return "Calm"
        elif 1 <= wind_speed < 6:
            return "Gentle breeze"
        elif 6 <= wind_speed < 10:
            return "Moderate gale"
        else:
            return "Storm"

    def create_weather_data_container(self, icon, value, category):
        """Create a container for weather data with an icon, value, and category."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=30, color="#0cb4cc"),  # Icon
                    ft.Text(value, size=16, weight="bold"),  # Value
                    ft.Text(category, size=12, color=ft.colors.BLACK),  # Category
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            border_radius=10,
            bgcolor=None,
        )

    def update_weather_ui(self, weather_data):
        """Update the UI with fetched weather data."""
        air_quality = weather_data.get("air_quality")
        temperature = weather_data.get("temperature")
        humidity = weather_data.get("humidity")
        uv_index = weather_data.get("uv_index")
        wind_speed = weather_data.get("wind_speed")

        if self.air_quality_container and air_quality:
            aqi = air_quality.get("indexes", [{}])[0].get("aqi", "N/A")
            category = self.categorize_aqi(aqi)
            self.air_quality_container.content.controls[1].value = str(aqi)  # Update value
            self.air_quality_container.content.controls[2].value = category  # Update category

        if self.temperature_container and temperature:
            temp_celsius = round(temperature - 273.15, 2) if temperature != "N/A" else "N/A"
            category = self.categorize_temp(temp_celsius)
            self.temperature_container.content.controls[1].value = f"{temp_celsius}°C"  # Update value
            self.temperature_container.content.controls[2].value = category  # Update category

        if self.humidity_container and humidity:
            category = self.categorize_humidity(humidity)
            self.humidity_container.content.controls[1].value = f"{humidity}%"  # Update value
            self.humidity_container.content.controls[2].value = category  # Update category

        if self.uv_index_container and uv_index:
            category = self.categorize_uv_index(uv_index)
            self.uv_index_container.content.controls[1].value = str(uv_index)  # Update value
            self.uv_index_container.content.controls[2].value = category  # Update category

        if self.wind_speed_container and wind_speed:
            category = self.categorize_wind_speed(wind_speed)
            self.wind_speed_container.content.controls[1].value = f"{wind_speed} m/s"  # Update value
            self.wind_speed_container.content.controls[2].value = category  # Update category

        # Update the page to reflect changes
        self.page.update()

    def create_nested_row(self, body_color, page, CONTAINER_TEXT1, CONTAINER_TEXT2, destination1, destination2, bg1, bg2):
        """Create a nested row with two containers that expand on hover."""
        def create_hoverable_container(content, destination, hover_color):
            """Create a container with hover scaling effect."""
            container = ft.Container(
                content=content,
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=body_color,
                border_radius=10,
                scale=ft.transform.Scale(scale=1),  # Initial scale
                animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),  # Smooth animation
            )

            def on_hover(e):
                """Handle hover events for the container."""
                if e.data == "true":
                    container.scale = ft.transform.Scale(scale=1.034)  # Scale up on hover
                else:
                    container.scale = ft.transform.Scale(scale=1)  # Reset scale on hover exit
                container.update()

            container.on_hover = on_hover

            if destination:
                container.on_click = lambda e: page.go(destination)  # Navigate on click

            return container

        return ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 6},
                    controls=[
                        create_hoverable_container(
                            content=ft.Stack([
                                ft.Image(
                                    src=f"src/assets/{bg1}.png",  # Replace with your image URL
                                    fit=ft.ImageFit.FIT_WIDTH,
                                    width=600,
                                ),
                                self.create_container(CONTAINER_TEXT1, bg1, destination=destination1, hover_color=ft.colors.GREEN_500)
                            ]),
                            destination=destination1,
                            hover_color=ft.colors.GREEN_500,
                        ),
                    ],
                ),
                ft.Column(
                    col={"sm": 12, "md": 6},
                    controls=[
                        create_hoverable_container(
                            content=ft.Stack([
                                ft.Image(
                                    src=f"src/assets/{bg2}.png",  # Replace with your image URL
                                    fit=ft.ImageFit.COVER,
                                    width=600,
                                ),
                                self.create_container(CONTAINER_TEXT2, bg2, destination=destination2, hover_color=ft.colors.GREEN_500)
                            ]),
                            destination=destination2,
                            hover_color=ft.colors.GREEN_500,
                        ),
                    ],
                ),
            ],
            expand=True,
        )

    def build(self):
        """Build and return the dashboard view."""
        print("Dashboard Loaded")

        # Create weather data containers
        self.air_quality_container = self.create_weather_data_container(ft.icons.CLOUD, "N/A", "N/A")
        self.temperature_container = self.create_weather_data_container(ft.icons.THERMOSTAT, "N/A", "N/A")
        self.humidity_container = self.create_weather_data_container(ft.icons.WATER_DROP, "N/A", "N/A")
        self.uv_index_container = self.create_weather_data_container(ft.icons.WB_SUNNY, "N/A", "N/A")
        self.wind_speed_container = self.create_weather_data_container(ft.icons.AIR, "N/A", "N/A")

        # Fetch weather data asynchronously
        self.page.run_task(self.controller.load_weather_data)

        # Nested column
        def create_nested_column(header_color, body_color, footer_color):
            return ft.Column(
                controls=[
                    ft.Container(
                        expand=3,
                        content=ft.Row(
                            controls=[
                                ft.Text(f"  Hello, {self.username if self.username else 'User'}!", size=20, weight="bold"),  # Display the username
                                ft.Row(
                                    controls=[
                                        self.air_quality_container,
                                        self.temperature_container,
                                        self.humidity_container,
                                        self.uv_index_container,
                                        self.wind_speed_container,
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        image_src="src/assets/USERBG.png", 
                        image_fit=ft.ImageFit.COVER,
                        padding=5,
                        alignment=ft.alignment.bottom_left,
                    ),
                    ft.Container(
                        expand=4,
                        content=self.create_nested_row(None, self.page, "Vaccination Schedules", "Health Resources", "/vaccination", "/health", "HEALTH", "VACCINATION SCHED"),
                        bgcolor=body_color,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        expand=4,
                        content=self.create_nested_row(None, self.page, "Statistics", "Infographics", "/stats", "/infographics", "STATS", "INFOGRAPHICS"),
                        bgcolor=body_color,
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
                    color="#0cb4cc", 
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
            appbar=self.DetailsAppBar(self.page, self),
            bgcolor="#f2f7ff",
        )

    def update_news(self, news_articles):
        """Update the news articles in the dashboard."""
        self.articles_section.controls[1].controls.clear()  # Clear the ListView
        for article in news_articles[:15]:  # Show first 15 articles
            self.articles_section.controls[1].controls.append(self.create_news_card(article))
        self.page.update()

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

    def create_container(self, text1, bg, destination=None, hover_color=None):
        """Create a hoverable container with a click event."""
        container = ft.Container(
            content=ft.Text(
                        text1, 
                        size=20,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
            border_radius=10,
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
            else:
                # Reset the container on hover exit
                container.scale = ft.transform.Scale(scale=1)
            container.update()

        container.on_hover = on_hover

        if destination:
            container.on_click = lambda e: self.controller.handle_navigation(destination)

        return container
    def show_username_dialog(self):
        """Display a dialog to change the username."""
        new_username_input = ft.TextField(label="Enter new username", autofocus=True)

        async def submit_username(e):
            new_username = new_username_input.value.strip()
            if new_username:
                response = await self.controller.update_username(self.username, new_username)
                if response:
                    self.username = new_username
                    self.page.snack_bar = ft.SnackBar(ft.Text("Username updated successfully!"))
                    self.page.update()
                    self.page.go(f"/home?username={new_username}")  # Refresh dashboard with new username
                else:
                    self.page.snack_bar = ft.SnackBar(ft.Text("Error updating username."))
                    self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Change Username"),
            content=new_username_input,
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.close_dialog()),
                ft.TextButton("Submit", on_click=submit_username),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


    class DetailsAppBar(ft.AppBar):

        def __init__(self, page, dashboard_view):
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
                    ft.Container(
                        content=ft.PopupMenuButton(
                            icon=ft.icons.SETTINGS,
                            icon_color="#0cb4cc",
                            items=[
                                ft.PopupMenuItem(
                                    text="Profile",
                                    on_click=lambda e: page.go("/profile"),  # Navigate to profile view
                                ),
                                ft.PopupMenuItem(
                                    text="Logout",
                                    on_click=lambda e: page.go("/login"),
                                ),
                            ],
                        ),
                        alignment=ft.alignment.center,
                    ),
                ],
            )
    async def load_news(self):
        """Load news articles asynchronously."""
        if self.news_controller:
            await self.news_controller.load_news()  # Call the correct method