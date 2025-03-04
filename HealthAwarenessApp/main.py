import flet as ft
from flet import *
from flet import Page, View, AppBar
from views.health_articles_view import HealthArticlesView
from views.article_details_view import ArticleDetailsView
from views.article_details_view import ArticleDetailsAppBar

from views.health_resources_view import HealthResourcesView
from views.resource_details_view import ResourceDetailsView
from views.resource_details_view import ResourceDetailsAppBar

from views.vaccination_stats_view import VaccinationStatsView
from views.vaccination_stats_view import StatsAppBar

from views.health_articles_view import ArticlesListAppBar
from views.health_resources_view import ResourcesListAppBar

def main(page: Page):
    page.route = "/resources"

    def route_change(route):
        page.views.clear()
        if page.route == "/articles":
            page.views.append(
                View(
                    "/articles",
                    appbar = ArticlesListAppBar(page),
                    controls=[HealthArticlesView(page)]
                )
            )
        elif page.route == "/article-details":
            page.views.append(
                View(
                    "/article-details",
                    appbar = ArticleDetailsAppBar(page),
                    controls=[ArticleDetailsView(page)]
                )
            )
        elif page.route == "/resources":
            page.views.append(
                View(
                    "/resources", 
                    appbar=ResourcesListAppBar(page),
                    controls=[
                        HealthResourcesView(page)
                    ]
                )
            )
        elif page.route == "/resource-details":
            page.views.append(
                View(
                    "/resource-details",
                    appbar=ResourceDetailsAppBar(page),
                    controls=[
                        ResourceDetailsView(page)
                    ]
                )
            )
            
        elif page.route == "/stats":
            page.views.append(
                View(
                    "/stats",
                    controls=[
                        StatsAppBar(page),
                        VaccinationStatsView(page)
                    ]
                )
            )
        # Add more routes for resources, resource details, etc.
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)