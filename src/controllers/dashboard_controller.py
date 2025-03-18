from pymongo import MongoClient

class DashboardController:
    def __init__(self, view, weather_controller):
        self.view = view
        self.weather_controller = weather_controller
        # MongoDB connection
        self.client = MongoClient("mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client.UserData_db
        self.users_collection = self.db.users

    def handle_navigation(self, destination):
        """Handle navigation to the specified destination."""
        self.view.navigate_to(destination)

    async def update_username(self, new_username):
        """Update the username in MongoDB."""
        if not new_username:
            return

        # Assuming the user's email or unique identifier is stored in the page object
        user_email = getattr(self.view.page, "email", None)
        if not user_email:
            print("User email not found.")
            return

        # Update the username in the MongoDB collection
        result = self.users_collection.update_one(
            {"email": user_email},  # Filter by user email
            {"$set": {"username": new_username}},  # Update the username
        )

        if result.modified_count > 0:
            print("Username updated successfully.")
        else:
            print("Failed to update username.")

    async def load_weather_data(self):
            """Load weather data asynchronously."""
            weather_data = await self.weather_controller.fetch_weather_data()
            if weather_data:
                self.view.update_weather_ui(weather_data)
