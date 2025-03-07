# src/controllers/dashboard_controller.py

class DashboardController:
    def __init__(self, view):
        self.view = view

    def handle_navigation(self, destination):
        """Handle navigation to the specified destination."""
        self.view.navigate_to(destination)