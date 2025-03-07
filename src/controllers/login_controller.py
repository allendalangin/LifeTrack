from src.models.login_model import UserModel  # Use absolute import

class LoginController:
    def __init__(self, view, users_collection):
        self.view = view
        self.model = UserModel(users_collection)

    def handle_login(self, username, password):
        success, message, username = self.model.authenticate_user(username, password)
        self.view.update_status(message)
        if success:
            self.view.navigate_to_home(username)