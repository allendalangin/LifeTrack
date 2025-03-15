# src/models/health_model.py

import time
import googlemaps
import requests

API_KEY = 'AIzaSyDaIfQ1cDwj4MaQcf-uuys1yJNx1fI-Tpg'  # Replace with your Google Maps API key

class HealthModel:
    def __init__(self):
        self.map_client = googlemaps.Client(API_KEY)  # Initialize the Google Maps client with the API key

    def miles_to_meters(self, miles):
        """Convert miles to meters."""
        try:
            return miles * 1_609.344
        except:
            return 0

    def get_user_location(self):
        """Get the user's current location using IP address via Google Maps Geolocation API."""
        try:
            # Prepare the request payload
            payload = {
                "considerIp": "true",  # Use IP address as a fallback
            }

            # Send the request to Google Maps Geolocation API
            url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"
            response = requests.post(url, json=payload)

            # Parse the response
            if response.status_code == 200:
                location = response.json()
                lat = location["location"]["lat"]
                lng = location["location"]["lng"]
                accuracy = location["accuracy"]
                print(f"Location found: Latitude={lat}, Longitude={lng}, Accuracy={accuracy} meters")
                return lat, lng
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None, None
        except Exception as e:
            print(f"Error retrieving location: {e}")
            return None, None

    def fetch_place_details(self, place_id):
        """Fetch detailed information about a place using its place_id."""
        try:
            place_details = self.map_client.place(
                place_id,
                fields=[
                    "name",
                    "formatted_address",
                    "rating",
                    "website",
                    "formatted_phone_number",
                    "opening_hours",
                    "photo",
                    "review",
                ]
            )
            return place_details.get('result', {})
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return {}

    def get_photo_url(self, photo_reference, max_width=400):
        """Generate a URL for a photo using its photo_reference."""
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={API_KEY}"  # Use the global API_KEY

    def search_nearby(self, lat, lng, mode):
        """Search for nearby places based on the mode (hospitals or pharmacies)."""
        if mode == "hospitals":
            search_keywords = ['hospital', 'clinic', 'medical centers']
        else:
            search_keywords = ['pharmacy', 'drug store']

        distance = self.miles_to_meters(2)
        business_list = []

        for search_string in search_keywords:
            response = self.map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )
            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = self.map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

        return business_list

    def fetch_autocomplete_suggestions(self, query):
        """Fetch autocomplete suggestions from the Google Places API."""
        if not query:
            return []

        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": query,
            "key": API_KEY,  # Use the global API_KEY
            "types": "geocode",  # Restrict to geographic locations
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("predictions", [])
        else:
            return []