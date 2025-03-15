import flet as ft
import webbrowser
from pymongo import MongoClient

class HealthView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.search_mode = "hospitals"  # Default search mode

        # UI Components
        self.fetching_data_text = ft.Text("", visible=True)  # Initially empty and hidden
        self.results_container = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=False)
        self.autocomplete_dropdown = ft.Column(visible=False, spacing=5)
        self.custom_location = ft.TextField(label="Enter a location",
                                            expand=True, 
                                            color="#0cb4cc",
                                            border_color="#0cb4cc",
                                            border_width=1,
                                            border_radius=10,
                                            label_style=ft.TextStyle(color="#0cb4cc"),
                                            on_change=self.on_search_change)
        self.search_mode_button = ft.ElevatedButton(
            "Search for Pharmacies/Drug Stores",
            on_click=self.toggle_search_mode,
        )

        # Containers for Hospital and Pharmacy Search
        self.hospital_container = self.create_selectable_container("Hospital Search", "#0cb4cc", self.select_hospital_mode)
        self.pharmacy_container = self.create_selectable_container("Pharmacy Search", "#0cb4cc", self.select_pharmacy_mode)

        # Hotlines Container
        self.hotlines_container = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )

        # Set default selected container to Hospital
        self.select_hospital_mode(None)  # Initialize with Hospital selected

        # Fetch hotline data on initialization
        self.page.run_task(self.fetch_hotlines)

    async def fetch_hotlines(self):
        """Fetch hotline data from MongoDB and display it in the hotlines container."""
        try:
            # Connect to MongoDB
            client = MongoClient("mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            db = client["health_resources"]
            collection = db["hotline"]

            # Fetch all hotline data with specific fields
            hotlines = list(collection.find({}, {"_id": 0, "department_name": 1, "phone_number": 1, "telephone_number": 1, "email": 1}))

            # Clear existing hotlines
            self.hotlines_container.controls.clear()

            # Add hotline data as cards
            for hotline in hotlines:
                department_name = hotline.get("department_name", "N/A")
                phone_number = hotline.get("phone_number", "N/A")
                telephone_number = hotline.get("telephone_number", "N/A")
                email = hotline.get("email", "N/A")

                hotline_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"Department: {department_name}", size=16, weight="bold"),
                                ft.Text(f"Phone Number: {phone_number}", size=14),
                                ft.Text(f"Telephone Number: {telephone_number}", size=14),
                                ft.Text(f"Email: {email}", size=14),
                            ],
                            spacing=5,
                        ),
                        padding=10,
                    ),
                    margin=5,
                )
                self.hotlines_container.controls.append(hotline_card)

            # Update the UI
            self.page.update()
        except Exception as e:
            print(f"Error fetching hotlines: {e}")
    # Helper function to create selectable containers
    def create_selectable_container(self, text, bgcolor, on_click):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=15),  # Container above the text
                    ft.Column(
                        controls=[
                            ft.Text(text, size=20, weight="bold"),
                            ft.Text("View " + text, size=16, color=ft.colors.GREY_600),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=15),  # Container below the text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border_radius=10,
            bgcolor=bgcolor,
            expand=True,
            alignment=ft.alignment.center,
            on_click=on_click,
            scale=ft.transform.Scale(scale=1),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )

    # Function to handle hospital mode selection
    def select_hospital_mode(self, e):
        self.search_mode = "hospitals"
        self.hospital_container.bgcolor = "#0a9eb8"  # Darken the color for selected
        self.pharmacy_container.bgcolor = "#0cb4cc"  # Reset pharmacy container color
        self.page.update()

    # Function to handle pharmacy mode selection
    def select_pharmacy_mode(self, e):
        self.search_mode = "pharmacies"
        self.pharmacy_container.bgcolor = "#0a9eb8"  # Darken the color for selected
        self.hospital_container.bgcolor = "#0cb4cc"  # Reset hospital container color
        self.page.update()

    # Function to toggle search mode (optional, if you still want the button)
    def toggle_search_mode(self, e):
        if self.search_mode == "hospitals":
            self.select_pharmacy_mode(e)
        else:
            self.select_hospital_mode(e)

    # Function to handle search bar changes
    def on_search_change(self, e):
        query = self.custom_location.value
        if query:
            suggestions = self.controller.fetch_autocomplete_suggestions(query)
            self.autocomplete_dropdown.controls.clear()
            for suggestion in suggestions:
                suggestion_text = suggestion.get("description", "")
                self.autocomplete_dropdown.controls.append(
                    ft.TextButton(
                        style=ft.ButtonStyle(color="#0cb4cc"),
                        text=suggestion_text,
                        on_click=lambda e, s=suggestion: self.select_suggestion(s),
                    )
                )
            self.autocomplete_dropdown.visible = True
        else:
            self.autocomplete_dropdown.visible = False
        self.page.update()

    # Function to handle suggestion selection
    def select_suggestion(self, suggestion):
        self.custom_location.value = suggestion.get("description", "")
        self.autocomplete_dropdown.visible = False
        self.page.update()

    # Function to show search results
    def show_results(self, business_list):
        self.results_container.controls.clear()  # Clear existing content
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
                                ft.TextButton(
                                    text=f"URL: {url}",
                                    on_click=lambda e, u=url: webbrowser.open(u),  # Open URL on click
                                    style=ft.ButtonStyle(color="#0cb4cc"),
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=5,
                    ),
                    margin=5,
                ),
                on_tap=lambda e, b=business: self.controller.show_place_details(b),
            )
            self.results_container.controls.append(result_card)

        # Reset scroll position to the top
        self.results_container.scroll_to(offset=0, duration=0)
        self.page.update()

    # Function to handle "Use Current Location" button click
    async def use_current_location(self, e):
        """Handle the 'Use Current Location' button click."""
        try:
            await self.controller.use_current_location()  # Perform the location search
        except Exception as ex:
            self.update_status(f"Error: {str(ex)}")  # Show error message
        finally:
            self.update_status("", visible=False)  # Hide the message after search is complete

    # Function to handle "Submit Custom Location" button click
    async def submit_custom_location(self, e):
        """Handle the 'Submit Custom Location' button click.""" # Show "Fetching results..." message
        try:
            location = self.custom_location.value
            if not location:  # Check if the location is empty
                self.update_status("Invalid Location")  # Show "Invalid Location" message
                return

            # Perform the location search
            await self.controller.submit_custom_location(location)
        except Exception as ex:
            self.update_status(f"Error: {str(ex)}")  # Show error message
        finally:
            self.update_status("", visible=False)  # Hide the message after search is complete

    # Function to toggle the visibility of the "Fetching data..." text
    def toggle_fetching_data(self, show):
        """Toggle the visibility of the 'Fetching data...' text."""
        self.fetching_data_text.visible = show
        self.page.update()  # Ensure the UI is updated

    # Function to show detailed information about a place
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

        # Details Column
        details_column = ft.Column(
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
                ft.Text("Reviews:", size=16, weight="bold"),
                ft.Column(
                    controls=[ft.Text(f"{review['author_name']}: {review['text']}", size=14) for review in reviews],
                    spacing=5,
                ),
            ],
            spacing=10,
            expand=True,
        )

        # Photos Column
        photos_column = ft.Column(
            controls=[
                ft.Text("Photos:", size=16, weight="bold"),
                ft.Column(
                    controls=[ft.Image(src=self.controller.model.get_photo_url(photo['photo_reference']), width=200, height=200) for photo in photos],
                    spacing=5,
                ),
            ],
            spacing=10,
            expand=True,
        )

        # Responsive Row for Layout
        responsive_row = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 8},
                    controls=[details_column],
                    expand=True,
                ),
                ft.Column(
                    col={"sm": 12, "md": 4},
                    controls=[photos_column],
                    expand=True,
                ),
            ],
            spacing=10,
            expand=True,
        )

        # Scrollable View
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
                    controls=[responsive_row],
                    expand=True,
                ),
            ],
        )

        self.page.views.append(details_view)
        self.page.update()

    # Function to build the view
    def build(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Search bar and buttons
        search_row = ft.Row(
            controls=[
                self.custom_location,
                ft.ElevatedButton("Use Current Location", on_click=self.use_current_location, color="#0cb4cc"),
                ft.ElevatedButton("Search Custom Location", on_click=self.submit_custom_location, color="#0cb4cc"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # Main layout
        main_layout = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 9},
                    controls=[
                        ft.Row(
                            controls=[self.hospital_container, self.pharmacy_container],
                            spacing=10,
                        ),
                        ft.Column(
                            controls=[
                                search_row,
                                self.autocomplete_dropdown,
                                self.fetching_data_text,  # Add fetching_data_text to the layout
                                ft.Container(
                                    content=self.results_container,
                                    expand=True,  # Allow the container to expand
                                    height=400,  # Set a fixed height or use expand=True
                                ),
                            ],
                            spacing=10,
                            expand=True,  # Ensure the Column expands to fill available space
                        ),
                    ],
                    expand=True,
                ),
                ft.Column(
                    col={"sm": 12, "md": 3},
                    controls=[
                        ft.Container(
                            content=self.hotlines_container,
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

        return ft.View(
            "/health",
            controls=[main_layout],
            appbar=self.DetailsAppBar(self.page),
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