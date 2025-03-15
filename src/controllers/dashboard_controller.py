<<<<<<< HEAD
from pymongo import MongoClient

class DashboardController:
    def __init__(self, view, weather_controller):
        self.view = view
        self.weather_controller = weather_controller
        # MongoDB connection
        self.client = MongoClient("mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client.UserData_db
        self.users_collection = self.db.users
=======
import httpx
>>>>>>> 5134dac723c5db5e2f5d079ca5f881af51480d4b

class DashboardController:
    def __init__(self, view):
        self.view = view
        self.api_url = "http://127.0.0.1:8000"

    def handle_navigation(self, destination):
        """Handle navigation to the specified destination."""
        self.view.navigate_to(destination)

<<<<<<< HEAD
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
=======
    async def update_username(self, old_username, new_username):
        """Call API to update username."""
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{self.api_url}/user/update_username",
                                        params={"old_username": old_username, "new_username": new_username})
            if response.status_code == 200:
                return True
            return False
>>>>>>> 5134dac723c5db5e2f5d079ca5f881af51480d4b
