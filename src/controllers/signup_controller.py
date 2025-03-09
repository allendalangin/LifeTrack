from src.models.login_model import UserModel  # Use absolute import

class SignupController:
    def __init__(self, view, users_collection):
        self.view = view
        self.model = UserModel(users_collection)

    def handle_signup(self, username, password, confirm_password):
        if password != confirm_password:
            self.view.update_status("Passwords do not match!", is_success=False)
            return

        success, message = self.model.register_user(username, password)
        self.view.update_status(message, is_success=success)
        if success:
            self.view.navigate_to_login()