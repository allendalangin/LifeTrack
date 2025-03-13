import flet as ft
import httpx
from src.models.login_model import UserModel
from src.models.health_model import HealthModel
from src.models.news_model import NewsModel
from src.models.stats_model import StatsModel
from src.controllers.login_controller import LoginController
from src.controllers.signup_controller import SignupController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.health_controller import HealthController
from src.controllers.news_controller import NewsController
from src.controllers.stats_controller import StatsController
from src.views.login_view import LoginView
from src.views.signup_view import SignupView
from src.views.dashboard_view import DashboardView
from src.views.health_view import HealthView
from src.views.news_view import NewsView
from src.views.stats_view import StatsView

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Google Maps API Key
API_KEY = 'AIzaSyDaIfQ1cDwj4MaQcf-uuys1yJNx1fI-Tpg'

# NewsAPI Key
NEWS_API_KEY = "373f805f1e35402bb154020a2aa70127"

def main(page: ft.Page):
    # Initialize the News Model and Controller
    news_model = NewsModel(NEWS_API_KEY)
    news_controller = NewsController(None, NEWS_API_KEY)

    # Initialize the Stats Model
    stats_model = StatsModel(FASTAPI_URL)

    async def route_change(route):
        print(f"Route changed to: {route}")
        page.views.clear()
        if page.route == "/login":
            print("Loading login view...")
            # Initialize the Model, Controller, and View for login
            model = UserModel(FASTAPI_URL)
            view = LoginView(page, None)
            controller = LoginController(view, FASTAPI_URL)
            view.controller = controller
            page.views.append(view.build())
        elif page.route == "/signup":
            print("Loading signup view...")
            # Initialize the Model, Controller, and View for signup
            model = UserModel(FASTAPI_URL)
            view = SignupView(page, None)
            controller = SignupController(view, FASTAPI_URL)
            view.controller = controller
            page.views.append(view.build())
        elif page.route.startswith("/home"):
            print("Loading dashboard...")
            username = None
            if "username=" in page.route:
                username = page.route.split("username=")[1]
            view = DashboardView(page, None, username, news_controller)
            controller = DashboardController(view)
            view.controller = controller
            page.views.append(view.build())
            page.run_task(view.load_news)
        elif page.route == "/health":
            print("Loading health resources...")
            model = HealthModel(API_KEY)
            view = HealthView(page, None)
            controller = HealthController(view, model)
            view.controller = controller
            page.views.append(view.build())
        elif page.route == "/news":
            print("Loading news view...")
            view = NewsView(page, news_controller)
            news_controller.view = view
            page.views.append(view.build())
            page.run_task(news_controller.load_news)
        elif page.route == "/stats":
            print("Loading statistics view...")
            view = StatsView(page, None)
            controller = StatsController(view, stats_model)
            view.controller = controller
            page.views.append(view.build())
        page.update()
        
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Set the initial route to "/login"
    page.route = "/login"
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main)