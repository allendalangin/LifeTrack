import flet as ft

class HealthView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.search_mode = "hospitals"  # Default search mode

        # UI Components
        self.fetching_data_text = ft.Text("Fetching data...", visible=False)  # Text to show when fetching data
        self.results_container = ft.ListView(expand=True, spacing=10, padding=20)
        self.autocomplete_dropdown = ft.Column(visible=False, spacing=5)
        self.custom_location = ft.TextField(hint_text="Enter a location", expand=True, on_change=self.on_search_change)
        self.search_mode_button = ft.ElevatedButton(
            "Search for Pharmacies/Drug Stores",
            on_click=self.toggle_search_mode,
        )
 #---------------------------------------OnClick Location Fetching--------------------------------------#
    async def use_current_location(self, e):
        """Handle the 'Use Current Location' button click."""
        self.toggle_fetching_data(True)  # Show the "Fetching data..." text
        try:
            await self.controller.use_current_location()  # Perform the location search
        finally:
            self.toggle_fetching_data(False)  # Hide the "Fetching data..." text

    async def submit_custom_location(self, e):
        """Handle the 'Submit Custom Location' button click."""
        self.toggle_fetching_data(True)  # Show the "Fetching data..." text
        try:
            await self.controller.submit_custom_location(self.custom_location.value)  # Perform the location search
        finally:
            self.toggle_fetching_data(False)  # Hide the "Fetching data..." text

 #---------------------------------------Container Template--------------------------------------#
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

#---------------------------------------AppBar Template--------------------------------------#
    class DetailsAppBar(ft.AppBar):
        """Custom app bar for the health resources view."""
        def __init__(self, page):
            super().__init__(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#0cb4cc",  # Set icon color to #0cb4cc
                    on_click=lambda e: page.go("/home"),  # Navigate to dashboard
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
 #---------------------------------------Health Resources View--------------------------------------#
    def build(self):
        """Build and return the health resources view."""
        self.page.title = "Location Search"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Layout
        search_row = ft.Row(
            controls=[self.custom_location, ft.ElevatedButton("Submit Custom Location", on_click=self.submit_custom_location)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # Main layout
        main_layout = ft.Column(
            controls=[
                ft.ElevatedButton("Use Current Location", on_click=self.use_current_location),
                self.search_mode_button,
                search_row,
                self.autocomplete_dropdown,
                self.fetching_data_text,  # Add the fetching data text
                self.results_container,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        # Use the custom app bar
        app_bar = self.DetailsAppBar(self.page)

        return ft.View(
            "/health",
            controls=[main_layout],
            appbar=app_bar,  # Set the custom app bar
        )
 #---------------------------------------Location Search--------------------------------------#
    def toggle_fetching_data(self, show):
        """Toggle the visibility of the 'Fetching data...' text."""
        self.fetching_data_text.visible = show
        self.page.update()  # Ensure the UI is updated

    async def use_current_location(self, e):
        """Handle the 'Use Current Location' button click."""
        self.toggle_fetching_data(True)  # Show the "Fetching data..." text
        try:
            await self.controller.use_current_location()  # Perform the location search
        finally:
            self.toggle_fetching_data(False)  # Hide the "Fetching data..." text

    async def submit_custom_location(self, e):
        """Handle the 'Submit Custom Location' button click."""
        self.toggle_fetching_data(True)  # Show the "Fetching data..." text
        try:
            await self.controller.submit_custom_location(self.custom_location.value)  # Perform the location search
        finally:
            self.toggle_fetching_data(False)  # Hide the "Fetching data..." text
 #---------------------------------------Search and AutoSuggestions--------------------------------------#
    def toggle_search_mode(self, e):
        """Handle the search mode toggle button click."""
        self.controller.toggle_search_mode()

    def on_search_change(self, e):
        """Handle changes in the search field and show autocomplete suggestions."""
        query = self.custom_location.value
        if query:
            suggestions = self.controller.fetch_autocomplete_suggestions(query)
            self.autocomplete_dropdown.controls.clear()
            for suggestion in suggestions:
                suggestion_text = suggestion.get("description", "")
                self.autocomplete_dropdown.controls.append(
                    ft.TextButton(
                        text=suggestion_text,
                        on_click=lambda e, s=suggestion: self.select_suggestion(s),
                    )
                )
            self.autocomplete_dropdown.visible = True
        else:
            self.autocomplete_dropdown.visible = False
        self.page.update()

    def select_suggestion(self, suggestion):
        """Handle selection of an autocomplete suggestion."""
        self.custom_location.value = suggestion.get("description", "")
        self.autocomplete_dropdown.visible = False
        self.page.update()
 #---------------------------------------Location Results--------------------------------------#
    def show_results(self, business_list):
        """Display search results in the UI."""
        self.results_container.controls.clear()
        for business in business_list:
            name = business.get('name', 'N/A')
            address = business.get('vicinity', 'N/A')
            rating = business.get('rating', 'N/A')
            place_id = business.get('place_id', 'N/A')
            url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            result_card = ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"Name: {name}", size=16, weight="bold"),
                                ft.Text(f"Address: {address}", size=14),
                                ft.Text(f"Rating: {rating}", size=14),
                                ft.Text(f"URL: {url}", size=14, color=ft.colors.BLUE),
                            ],
                            spacing=5,
                        ),
                        padding=10,
                    ),
                    margin=5,
                ),
                on_tap=lambda e, b=business: self.controller.show_place_details(b),
            )
            self.results_container.controls.append(result_card)
        self.page.update()

    def show_place_details(self, place_details):
        """Show detailed information about a place."""
        name = place_details.get('name', 'N/A')
        address = place_details.get('formatted_address', 'N/A')
        rating = place_details.get('rating', 'N/A')
        phone_number = place_details.get('formatted_phone_number', 'N/A')
        website = place_details.get('website', 'N/A')
        opening_hours = place_details.get('opening_hours', {}).get('weekday_text', [])
        photos = place_details.get('photos', [])
        reviews = place_details.get('reviews', [])

        details_view = ft.View(
            "/place_details",
            controls=[
                ft.AppBar(
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
                color="#0cb4cc",
                ),
                ft.ListView(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"Name: {name}", size=20, weight="bold"),
                                ft.Text(f"Address: {address}", size=16),
                                ft.Text(f"Rating: {rating}", size=16),
                                ft.Text(f"Phone: {phone_number}", size=16),
                                ft.Text(f"Website: {website}", size=16, color=ft.colors.BLUE),
                                ft.Text("Opening Hours:", size=16, weight="bold"),
                                ft.Column(
                                    controls=[ft.Text(hour, size=14) for hour in opening_hours],
                                    spacing=5,
                                ),
                                ft.Text("Photos:", size=16, weight="bold"),
                                ft.Column(
                                    controls=[ft.Image(src=self.controller.model.get_photo_url(photo['photo_reference']), width=200, height=200) for photo in photos],
                                    spacing=5,
                                ),
                                ft.Text("Reviews:", size=16, weight="bold"),
                                ft.Column(
                                    controls=[ft.Text(f"{review['author_name']}: {review['text']}", size=14) for review in reviews],
                                    spacing=5,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                ),
            ],
        )

        self.page.views.append(details_view)
        self.page.update()
 
    def update_status(self, message):
        """Update the status message in the UI."""
        self.results_container.controls.append(ft.Text(message, color=ft.colors.RED))
        self.page.update()
 #---------------------------------------Search Mode--------------------------------------#
    def update_search_mode_button(self, search_mode):
        """Update the search mode button text."""
        if search_mode == "hospitals":
            self.search_mode_button.text = "Search for Pharmacies/Drug Stores"
        else:
            self.search_mode_button.text = "Search for Hospitals/Clinics"
        self.page.update()