import flet as ft
from flet import Text, Container, SearchBar, border, Column, ListView, alignment, MainAxisAlignment, CrossAxisAlignment, AppBar, PopupMenuButton, PopupMenuItem, ElevatedButton
import requests
from models.resource import Resource

#ListAppBar
class ResourcesListAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            title = Text("LifeTrack"),
            actions=[
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Dashboard"),
                        PopupMenuItem(text="Health Articles", on_click = lambda _: page.go("/articles")),
                        PopupMenuItem(text="Health Resources", on_click = lambda _: page.go("/resources")),
                        PopupMenuItem(text="Stats"),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )

# Helper function to fetch resources from the API endpoint
def fetch_resources():
    try:
        response = requests.get("http://127.0.0.1:8000/resources")
        if response.status_code == 200:
            return response.json()  # Expecting a list of resource dictionaries
        else:
            print("Server returned status code", response.status_code)
            return []
    except Exception as e:
        print("Error fetching resources:", e)
        return []

# Convert a dictionary (from API) to a Resource model instance
def dict_to_resource(resource_dict):
    return Resource(
        name=resource_dict.get("name", ""),
        category=resource_dict.get("category", ""),
        location=resource_dict.get("location", "")
    )

# UI component for a single resource
class HealthResourceView(Container):
    def __init__(self, resource: Resource, page=None):
        super().__init__()
        self.page = page
        self.resource = resource

    def build_container(self, page=None):
        nav_page = page or self.page
        return Container(
            content=Column(controls=[
                Text(self.resource.name, size=18, weight="bold"),
                Text(self.resource.category, size=18),
                Text(self.resource.location, size=16, weight="italic"),
            ]),
            padding=10,
            border=border.all(1, "white"),
            border_radius=20,
            width=550,
            height=120,
            ink=True,
            on_click=lambda _: (
                setattr(nav_page, "selected_resource", self.resource),
                nav_page.go("/resource-details"))
        )

def HealthResourcesView(page: ft.Page):
    page.title = "Health Resources"
    page.theme_mode = "dark"
    page.scroll = True
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Fetch resources from the FastAPI backend
    resources_data = fetch_resources()
    resources = [dict_to_resource(rd) for rd in resources_data]

    # Build a ListView of resource UI elements
    resources_list = ListView(
        expand=True,
        spacing=20,
        width=600,
        controls=[HealthResourceView(resource, page).build_container(page) for resource in resources]
    )

    # Function to filter resources based on the search query
    def update_list(query):
        filtered = [resource for resource in resources if query.lower() in resource.name.lower()]
        resources_list.controls = [HealthResourceView(resource, page).build_container(page) for resource in filtered]
        page.update()

    # Build the search bar
    search_bar = SearchBar(
        bar_hint_text="Search resources...",
        width=600,
        height=50,
        on_change=lambda e: update_list(e.control.value)
    )

    return Column(
        controls=[
            Container(content=search_bar, margin=20, alignment=ft.alignment.center),
            Container(content=resources_list, height=600, margin=20, alignment=alignment.center),
        ],
        alignment=MainAxisAlignment.CENTER
    )
