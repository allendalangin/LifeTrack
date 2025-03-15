import httpx

class DashboardController:
    def __init__(self, view):
        self.view = view
        self.api_url = "http://127.0.0.1:8000"

    def handle_navigation(self, destination):
        """Handle navigation to the specified destination."""
        self.view.navigate_to(destination)

    async def update_username(self, old_username, new_username):
        """Call API to update username."""
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{self.api_url}/user/update_username",
                                        params={"old_username": old_username, "new_username": new_username})
            if response.status_code == 200:
                return True
            return False
