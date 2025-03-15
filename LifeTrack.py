# lifetrack.py
import flet as ft
import httpx
from urllib.parse import urlparse, parse_qs
from src.models.login_model import UserModel
from src.models.health_model import HealthModel
from src.models.stats_model import StatsModel
from src.models.infographics_model import InfographicsModel
from src.views.vaccination_schedule_view import VaccinationScheduleView

from src.controllers.login_controller import LoginController
from src.controllers.signup_controller import SignupController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.health_controller import HealthController
from src.controllers.article_controller import ArticleController
from src.controllers.stats_controller import StatsController
from src.controllers.weather_controller import WeatherController  
from src.controllers.infographics_controller import InfographicsController

from src.views.login_view import LoginView
from src.views.signup_view import SignupView
from src.views.dashboard_view import DashboardView
from src.views.health_view import HealthView
from src.views.stats_view import StatsView
from src.views.health_articles_view import HealthArticlesView
from src.views.article_details_view import ArticleDetailsView
from src.views.infographics_view import InfographicsView


FASTAPI_URL = "http://127.0.0.1:8000"
NEWS_API_KEY = "5111ef64cdb0c0c8bc6e35bcef2f82e5"
GOOGLE_API_KEY = "AIzaSyBw00vdMc_H8vWKsFvjnflI37NnZB0mrLM"
OPENWEATHERMAP_API_KEY = "7dec04c1fa4aac28978bd98f42ba4f7a"

def main(page: ft.Page):
    # Initialize the Article Controller
    article_controller = ArticleController(NEWS_API_KEY)

    # Initialize the Weather Controller
    weather_controller = WeatherController(GOOGLE_API_KEY, OPENWEATHERMAP_API_KEY)

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
        elif page.route == "/home":
            print("Loading dashboard...")
            # Fetch username from the page object
            username = getattr(page, "username", None)  # Get username or None if not set

            view = DashboardView(page, None, article_controller)
            controller = DashboardController(view, weather_controller)  # Pass weather_controller
            view.controller = controller
            page.views.append(view.build())
            page.run_task(view.load_news)  # Load news articles
            page.run_task(controller.load_weather_data)  # Load weather data
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
            # Extract username from query parameters
            parsed_url = urlparse(page.route)  # Use urlparse
            query_params = parse_qs(parsed_url.query)  # Use parse_qs
            username = query_params.get("username", [None])[0]
            # If username is not in the route, fetch it from the page object
            if username is None and hasattr(page, "username"):
                username = page.username

            view = DashboardView(page, None, username, article_controller)
            controller = DashboardController(view, weather_controller)  # Pass weather_controller
            view.controller = controller
            page.views.append(view.build())
            page.run_task(view.load_news)  # Load news articles
            page.run_task(controller.load_weather_data)  # Load weather data
        elif page.route == "/health":
            print("Loading health resources...")
            model = HealthModel()
            view = HealthView(page, None)
            controller = HealthController(view, model)
            view.controller = controller
            page.views.append(view.build())
        elif page.route == "/news":
            print("Loading news view...")
            view = HealthArticlesView(page, article_controller)
            page.views.append(view)
            page.run_task(view.fetch_and_display_articles)
        elif page.route == "/article-details":
            # Load article details view
            view = ArticleDetailsView(page)
            page.views.append(view)
        elif page.route == "/stats":
            print("Loading statistics view...")
            view = StatsView(page, None)
            controller = StatsController(view, StatsModel())
            view.controller = controller
            page.views.append(view.build())
        elif page.route == "/infographics":
            print("Loading infographics view...")
            view = InfographicsView(page)  # Initialize InfographicsView
            controller = InfographicsController(view)  # Initialize InfographicsController
            view.controller = controller  # Assign controller to view
            page.views.append(view.build())  # Build and append the view
            page.run_task(controller.load_infographics)  # Load infographics
        elif page.route == "/vaccination":
            print("Loading vaccination schedule view...")
            view = VaccinationScheduleView(page)  # Initialize VaccinationScheduleView
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