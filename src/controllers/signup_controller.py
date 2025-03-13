# src/controllers/signup_controller.py

from src.models.login_model import UserModel

class SignupController:
    def __init__(self, view, api_url):
        self.view = view
        self.model = UserModel(api_url)

    async def handle_signup(self, username, password, confirm_password):
        if password != confirm_password:
            self.view.update_status("Passwords do not match!", is_success=False)
            return

        success, message = await self.model.register_user(username, password)
        self.view.update_status(message, is_success=success)
        if success:
            self.view.navigate_to_login()