# src/controllers/login_controller.py

from src.models.login_model import UserModel

class LoginController:
    def __init__(self, view, api_url):
        self.view = view
        self.model = UserModel(api_url)

    async def handle_login(self, username, password):
        success, message, username = await self.model.authenticate_user(username, password)
        self.view.update_status(message)
        if success:
            self.view.page.username = username  # Store the username in the page object
            self.view.navigate_to_home()