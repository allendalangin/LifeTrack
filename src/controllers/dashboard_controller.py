from pymongo import MongoClient
import httpx

class DashboardController:
    def __init__(self, view, weather_controller):
        self.view = view
        self.weather_controller = weather_controller

        # MongoDB connection
        self.client = MongoClient("mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client.UserData_db  # Your MongoDB database name
        self.users_collection = self.db.users  # Your users collection

        # API URL (for potential username update via API)
        self.api_url = "http://127.0.0.1:8000"

    def handle_navigation(self, destination):
        """Handle navigation to the specified destination."""
        self.view.navigate_to(destination)
        
    async def load_weather_data(self):
        """Load weather data asynchronously and update the dashboard view."""
        weather_data = await self.weather_controller.fetch_weather_data()
        
        if weather_data:
            print("Weather data fetched:", weather_data)
            # Pass the weather data to the view to update the UI
            self.view.update_weather_ui(weather_data)
        else:
            print("Failed to fetch weather data.")

    async def update_username_in_db(self, new_username):
        """Update the username in MongoDB."""
        if not new_username:
            print("No new username provided")
            return

        current_username = self.view.username  # Fetch the current username from the view
        if current_username == new_username:
            print("The new username is the same as the current username. No update needed.")
            return  # Skip update if the username hasn't changed

        # Proceed with the update only if the new username is different
        result = self.users_collection.update_one(
            {"username": current_username},  # Find the user by the current username
            {"$set": {"username": new_username}}  # Set the new username
        )

        if result.modified_count > 0:
            print("Username updated successfully.")
            self.view.username = new_username  # Update the view with the new username
        else:
            print("Failed to update username.")
