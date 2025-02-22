import flet as ft
from flet import *
from flet import Text, Container, SearchBar, border
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment

class HealthResource(Container):
    def __init__(self, page, name: str, type: str, location: str) -> None:
        super().__init__()
        self.page = page
        self.name = name
        self.type = type
        self.location = location

    def build_container(self):
        print(f"Building container for: {self.name}")  # Debug print to see if this method is called
        return Container(
            content=Column(controls=[
                Text(self.name, size=18, weight="bold"),
                Text(self.type, size=18),
                Text(self.location, size=16, weight="italic"),
            ]),
            padding=10,
            border=border.all(1, "white"),
            border_radius=20,
            width=550,
            height=120,
            ink=True,
            on_click=lambda _: self.page.go("/details")
        )
    
    @classmethod
    def build_list(cls, resources):
        list_view = ListView(
            expand=True,
            spacing=20,
            width=600,
        )
        for resource in resources:
            list_view.controls.append(resource.build_container())

        return list_view

def HealthResourcesView(page):
    page.title = "Health Resources"
    page.theme_mode = "dark"
    page.scroll = True
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    
    # Function to filter resources
    def filter_resources(query):
        return [resource for resource in resources if query.lower() in resource.name.lower()]

    # Function to update the list based on the search query
    def update_list(query):
        filtered_resources = filter_resources(query)
        health_resources_list.controls = [resource.build_container() for resource in filtered_resources]
        page.update()

    # Data for health resources
    resources = [
        HealthResource(page, "St. Luke’s Medical Center", "Hospital", "Quezon City"),
        HealthResource(page, "Makati Medical Center", "Hospital", "Makati City"),
        HealthResource(page, "Health First Clinic", "Clinic", "Pasig City"),
        HealthResource(page, "GreenLife Pharmacy", "Pharmacy", "Taguig City"),
    ]

    # Build controls
    search_bar = SearchBar(
        bar_hint_text="Search articles...",
        width=600,
        height=50,
        on_change=lambda e: update_list(e.control.value)
    )

    health_resources_list = HealthResource.build_list(resources)

    return Column(
            controls=[
                Container(content=search_bar, margin=20, alignment=ft.alignment.center),
                Container(content=health_resources_list, height=600, margin=20, alignment=alignment.center),
            ],
            alignment=MainAxisAlignment.CENTER
        )

if __name__ == "__main__":
    ft.app(main)
