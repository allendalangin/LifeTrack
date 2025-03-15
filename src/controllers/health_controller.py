class HealthController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.search_mode = "hospitals"  # Default search mode

    async def use_current_location(self):
        """Search for nearby places using the user's current location."""
        self.view.toggle_fetching_data(True)  # Show loading progress bar
        lat, lng = self.model.get_user_location()  # Get the user's location using IP-based geolocation
        if lat and lng:
            business_list = self.model.search_nearby(lat, lng, self.search_mode)
            self.view.show_results(business_list)
        else:
            self.view.update_status("Unable to retrieve current location.")
        self.view.toggle_fetching_data(False)  # Hide loading progress bar

    async def submit_custom_location(self, location):
        """Search for nearby places using a custom location."""
        if location:
            self.view.toggle_fetching_data(True)  # Show loading progress bar
            geocode = self.model.map_client.geocode(address=location)
            if geocode:
                lat, lng = map(lambda x: geocode[0]['geometry']['location'][x], ('lat', 'lng'))
                business_list = self.model.search_nearby(lat, lng, self.search_mode)
                self.view.show_results(business_list)
            else:
                self.view.update_status("Invalid location.")
            self.view.toggle_fetching_data(False)  # Hide loading progress bar
        else:
            self.view.update_status("Please enter a location.")

    def toggle_search_mode(self):
        """Toggle between searching for hospitals/clinics and pharmacies/drug stores."""
        if self.search_mode == "hospitals":
            self.search_mode = "pharmacies"
        else:
            self.search_mode = "hospitals"
        self.view.update_search_mode_button(self.search_mode)

    def fetch_autocomplete_suggestions(self, query):
        """Fetch autocomplete suggestions for the search field."""
        return self.model.fetch_autocomplete_suggestions(query)

    def show_place_details(self, business):
        """Show detailed information about a place."""
        place_details = self.model.fetch_place_details(business.get('place_id', 'N/A'))
        self.view.show_place_details(place_details)