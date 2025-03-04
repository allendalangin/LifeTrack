import time
import googlemaps
import requests
import flet as ft

def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data.get('loc', '').split(',')
        if len(location) == 2:
            latitude, longitude = location
            return float(latitude), float(longitude)
        else:
            return None, None
    except Exception as e:
        print(f"Error retrieving location: {e}")
        return None, None

# Initialize the Google Maps client outside of functions
API_KEY = 'AIzaSyDaIfQ1cDwj4MaQcf-uuys1yJNx1fI-Tpg'  # Replace with your actual API key
map_client = googlemaps.Client(API_KEY)

def create_location_search_view(page):
    page.title = "Location Search"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Add a progress bar
    progress_bar = ft.ProgressBar(value=0, visible=False)
    results_container = ft.ListView(expand=True, spacing=10, padding=20)  # Scrollable container for results
    autocomplete_dropdown = ft.Column(visible=False, spacing=5)  # Dropdown for autocomplete suggestions

    # Variable to track the current search mode
    search_mode = "hospitals"  # Default to searching for hospitals/clinics

    def toggle_loading(show):
        """Toggle the visibility of the loading progress bar."""
        progress_bar.visible = show
        page.update()

    def update_progress(value):
        """Update the progress bar's value."""
        progress_bar.value = value
        page.update()

    def clear_results():
        """Clear the results container."""
        results_container.controls.clear()
        page.update()

    def use_current_location(e):
        clear_results()  # Clear previous results
        toggle_loading(True)  # Show loading progress bar
        lat, lng = get_user_location()
        if lat and lng:
            search_nearby(lat, lng, search_mode)
        else:
            print("Unable to retrieve current location.")
        toggle_loading(False)  # Hide loading progress bar

    def search_nearby(lat, lng, mode):
        if mode == "hospitals":
            search_keywords = ['hospital', 'clinic', 'medical centers']
        else:
            search_keywords = ['pharmacy', 'drug store']

        distance = miles_to_meters(2)
        business_list = []

        total_keywords = len(search_keywords)
        for index, search_string in enumerate(search_keywords):
            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )
            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            # Update progress bar
            update_progress((index + 1) / total_keywords)

        # Display results in the UI
        for business in business_list:
            name = business.get('name', 'N/A')
            address = business.get('vicinity', 'N/A')
            rating = business.get('rating', 'N/A')
            place_id = business.get('place_id', 'N/A')
            url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            # Create a card for each result
            result_card = ft.Card(
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
            )
            results_container.controls.append(result_card)

        page.update()  # Update the UI with new results

    def fetch_autocomplete_suggestions(query):
        """Fetch autocomplete suggestions from the Google Places API."""
        if not query:
            return []

        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": query,
            "key": API_KEY,
            "types": "geocode",  # Restrict to geographic locations
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("predictions", [])
        else:
            return []

    def on_search_change(e):
        """Handle changes in the search field and show autocomplete suggestions."""
        query = custom_location.value
        if query:
            suggestions = fetch_autocomplete_suggestions(query)
            autocomplete_dropdown.controls.clear()
            for suggestion in suggestions:
                suggestion_text = suggestion.get("description", "")
                autocomplete_dropdown.controls.append(
                    ft.TextButton(
                        text=suggestion_text,
                        on_click=lambda e, s=suggestion: select_suggestion(s),
                    )
                )
            autocomplete_dropdown.visible = True
        else:
            autocomplete_dropdown.visible = False
        page.update()

    def select_suggestion(suggestion):
        """Handle selection of an autocomplete suggestion."""
        custom_location.value = suggestion.get("description", "")
        autocomplete_dropdown.visible = False
        page.update()

    def submit_custom_location(e):
        if custom_location.value:
            clear_results()  # Clear previous results
            toggle_loading(True)  # Show loading progress bar
            geocode = map_client.geocode(address=custom_location.value)
            if geocode:
                lat, lng = map(lambda x: geocode[0]['geometry']['location'][x], ('lat', 'lng'))
                search_nearby(lat, lng, search_mode)
            else:
                print("Invalid location.")
            toggle_loading(False)  # Hide loading progress bar
        else:
            print("Please enter a location.")

    def toggle_search_mode(e):
        """Toggle between searching for hospitals/clinics and pharmacies/drug stores."""
        nonlocal search_mode
        if search_mode == "hospitals":
            search_mode = "pharmacies"
            search_mode_button.text = "Search for Pharmacies/Drug Stores"
        else:
            search_mode = "hospitals"
            search_mode_button.text = "Search for Hospitals/Clinics"
        page.update()

    # Back to Dashboard Button
    back_to_dashboard_btn = ft.ElevatedButton(
        "Back to Dashboard",
        on_click=lambda e: page.go("/home"),  # Navigate to /home
    )

    # UI Components
    current_location_btn = ft.ElevatedButton("Use Current Location", on_click=use_current_location)
    custom_location = ft.TextField(hint_text="Enter a location", expand=True, on_change=on_search_change)
    submit_location_btn = ft.ElevatedButton("Submit Custom Location", on_click=submit_custom_location)
    search_mode_button = ft.ElevatedButton("Search for Pharmacies/Drug Stores", on_click=toggle_search_mode)

    # Layout
    search_row = ft.Row(
        controls=[custom_location, submit_location_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Main layout
    main_layout = ft.Column(
        controls=[
            back_to_dashboard_btn,  # Add the back button at the top
            current_location_btn,
            search_mode_button,  # Button to toggle search mode
            search_row,
            autocomplete_dropdown,  # Autocomplete suggestions dropdown
            progress_bar,  # Progress bar for loading
            results_container,  # Scrollable container for results
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,  # Ensure the layout expands to fill available space
    )

    return ft.View(
        "/health",
        controls=[main_layout],
    )