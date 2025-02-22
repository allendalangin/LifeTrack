import flet as ft
from flet import Page, View
from HealthResources import HealthResourcesView
from Details import DetailsView

def main(page: Page):
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                View(
                    "/", controls=[
                        HealthResourcesView(page)
                    ]
                )
            )
        elif page.route == "/details":
            page.views.append(
                View(
                    "/details",controls=[
                        DetailsView(page)
                    ]
                )
            )
        page.update()
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)