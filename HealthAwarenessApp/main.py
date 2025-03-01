import flet as ft
from flet import *
from flet import Page, View, AppBar
from views.heath_
from views.article_details_view import ArticleDetailsView
from views.article_details_view import ArticleDetailsAppBar
from views.health_resources_view import HealthResourcesView
from views.resource_details_view import ResourceDetailsView
from views.resource_details_view import ResourceDetailsAppBar

def main(page: Page):
    page.route = "/resources"

    def route_change(route):
        page.views.clear()
        if page.route == "/articles":
            page.views.append(
                View(
                    "/articles",
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
                    "/resources", controls=[
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
        # Add more routes for resources, resource details, etc.
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)