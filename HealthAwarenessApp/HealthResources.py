#TODO: ADD ONCLICK FUNCTION AND FILTERS

import flet as ft
from flet import Text, Colors, ElevatedButton, Container, IconButton, SearchBar, border
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Row, Column, ListView, alignment

class HealthResource(Container):
    def __init__(self, name:str, type:str, location:str)->None:
        super().__init__()
        self.name = name
        self.type = type
        self.location = location
    
    def build_container(self):
        return Container(
            content=Column(controls=[
                Text(self.name, size=18, weight="bold"),
                Text(self.type, size=18),
                Text(self.location, size=16, weight="italic"),
            ]),
            padding=10,
            border=border.all(1,"white"),
            border_radius=20,
            width=550,
            height=120,
        )
    
    @classmethod #to make this a class method, no need to make object
    def build_list(cls, resources):
        list_view = ListView(
            expand=True,
            spacing=20,
            width=600,
        )
        for resource in resources:
            list_view.controls.append(resource.build_container())

        return list_view

def main(page: Page)->None:
    page.title = "Health Resources"
    page.theme_mode = "dark"
    page.scroll = True
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    
    #data for health resources
    resources = [
        HealthResource("St. Luke’s Medical Center", "Hospital", "Quezon City"),
        HealthResource("Makati Medical Center", "Hospital", "Makati City"),
        HealthResource("Health First Clinic", "Clinic", "Pasig City"),
        HealthResource("GreenLife Pharmacy", "Pharmacy", "Taguig City"),
    ]

    #build controls
    search_bar = SearchBar(
        bar_hint_text=
        "Search articles...",
        width=600,
        height=50,
    )

    health_resources_list = HealthResource.build_list(resources)

    page.add(
        Column(
            controls=[
                Container(content=search_bar,
                margin=20,
                alignment=ft.alignment.center
                ),
                Container(content=health_resources_list,
                height=600,
                margin=20,
                alignment=alignment.center
                ),
            ],
            alignment=MainAxisAlignment.CENTER
            
        )
    )

if __name__ == "__main__":
    ft.app(main)