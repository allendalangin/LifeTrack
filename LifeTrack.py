# src/main.py

import flet as ft
import pymongo
from src.models.login_model import UserModel
from src.models.health_model import HealthModel
from src.controllers.login_controller import LoginController
from src.controllers.signup_controller import SignupController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.health_controller import HealthController
from src.views.login_view import LoginView
from src.views.signup_view import SignupView
from src.views.dashboard_view import DashboardView
from src.views.healthview import HealthView

# MongoDB Connection (Replace with your MongoDB URI)
MONGO_URI = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client["UserData_db"]  # Database name
users_collection = db["users"]  # Collection name

# Google Maps API Key
API_KEY = 'AIzaSyDaIfQ1cDwj4MaQcf-uuys1yJNx1fI-Tpg'  # Replace with your actual API key

# src/main.py

def main(page: ft.Page):
    def route_change(route):
        print(f"Route changed to: {route}")  # Debugging
        page.views.clear()
        if page.route == "/login":
            print("Loading login view...")  # Debugging
            # Initialize the Model, Controller, and View for login
            model = UserModel(users_collection)
            view = LoginView(page, None)
            controller = LoginController(view, users_collection)
            view.controller = controller
            page.views.append(view.build())
        elif page.route == "/signup":
            print("Loading signup view...")  # Debugging
            # Initialize the Model, Controller, and View for signup
            model = UserModel(users_collection)
            view = SignupView(page, None)
            controller = SignupController(view, users_collection)
            view.controller = controller
            page.views.append(view.build())
        elif page.route.startswith("/home"):
            print("Loading dashboard...")  # Debugging
            # Initialize the Controller and View for dashboard
            username = None
            if "username=" in page.route:
                username = page.route.split("username=")[1]
            view = DashboardView(page, None, username)
            controller = DashboardController(view)
            view.controller = controller
            page.views.append(view.build())
        elif page.route == "/health":
            print("Loading health resources...")
            # Initialize the Model, Controller, and View for health resources
            model = HealthModel(API_KEY)
            view = HealthView(page, None)
            controller = HealthController(view, model)
            view.controller = controller
            page.views.append(view.build())
        page.update()
        
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Set the initial route to "/login"
    page.route = "/login"  # Explicitly set the route
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")  # Navigate to the login page

ft.app(target=main)