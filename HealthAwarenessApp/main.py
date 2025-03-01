import flet as ft
from flet import Page, View
from HealthResources import HealthResourcesView
from HealthArticles import HealthArticlesView
from ResourceDetails import ResourceDetailsView
from ResourceDetails import ResourceDetailsAppBar
from ArticleDetails import ArticleDetailsView
from ArticleDetails import ArticleDetailsAppBar

def main(page: Page):
    page.route = "/articles"
    def route_change(route):
        page.views.clear()
        if page.route == "/resources":
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
        elif page.route == "/articles":
            page.views.append(
                View(
                    "/articles",
                    controls=[
                        HealthArticlesView(page)
                    ]
                )
            )
        elif page.route == "/article-details":
            page.views.append(
                View(
                    "/article-details",
                    appbar=ArticleDetailsAppBar(page),
                    controls=[
                        ArticleDetailsView(page)
                    ]
                )
            )
        page.update()
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)