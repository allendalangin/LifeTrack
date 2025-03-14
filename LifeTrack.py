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
from src.controllers.article_controller import ArticleController
from src.controllers.stats_controller import StatsController
from src.views.login_view import LoginView
from src.views.signup_view import SignupView
from src.views.dashboard_view import DashboardView
from src.views.health_view import HealthView
from src.views.stats_view import StatsView
from src.views.health_articles_view import HealthArticlesView
from src.views.article_details_view import ArticleDetailsView
# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# NewsAPI Key
NEWS_API_KEY = "5111ef64cdb0c0c8bc6e35bcef2f82e5"

def main(page: ft.Page):
    # Initialize the Article Controller
    article_controller = ArticleController(NEWS_API_KEY)

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
            view = DashboardView(page, None, username, article_controller)
            controller = DashboardController(view)
            view.controller = controller
            page.views.append(view.build())
            page.run_task(view.load_news)  # Load news articles
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