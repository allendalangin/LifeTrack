# src/controllers/admin_login_controller.py

from src.models.admin_login_model import AdminLoginModel

class AdminLoginController:
    def __init__(self, view, api_url):
        self.view = view
        self.model = AdminLoginModel(api_url)

    async def handle_admin_login(self, username, password):
        # Authenticate the admin
        success, message, username = await self.model.authenticate_admin(username, password)
        self.view.update_status(message)
        if success:
            self.view.page.username = username  # Store the username in the page object
            self.view.navigate_to_admin_panel()