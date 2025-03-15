import flet as ft
from flet import *
from src.controllers.vaccination_schedule_controller import VaccinationScheduleController

class DetailsAppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color="#0cb4cc",
                on_click=lambda e: page.go("/home"),
            ),
            title=ft.Column(
                controls=[
                    ft.Container(height=3),
                    ft.Image(
                        src="src/assets/LifeTrackLogo.png",
                        height=55,
                        fit=ft.ImageFit.FIT_HEIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            center_title=True,
            toolbar_height=50,
            elevation=4,  # Add elevation for shadow
        )

class VaccinationScheduleView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/vaccination")
        self.page = page
        self.controller = VaccinationScheduleController()
        self.controls = self.build()

    def build(self):
        """Build the vaccination schedule view."""
        schedule_data = self.controller.fetch_schedules()
        schedule_controls = self.build_schedule_list(schedule_data)

        return [
            DetailsAppBar(self.page),  # Add the app bar
            Container(
                width=self.page.width,  # Use full page width
                height=self.page.height,  # Use full page height
                padding=20,
                alignment=ft.alignment.center,  # Center the container
                content=Column(
                    controls=[
                        Divider(height=20, color="transparent"),
                        self.create_main_container(),
                        Divider(height=0, color="white24"),
                    ]
                    + schedule_controls,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center children horizontally
                ),
            ),
        ]

    def create_main_container(self):
        """Create the main container for the vaccination schedule view."""
        return Container(
            width=275,
            height=60,
            alignment=ft.alignment.center,  # Center the content
            content=Column(
                spacing=3,
                alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
                controls=[
                    Text("Health Is Wealth", size=12, weight="W_400", color=ft.colors.BLACK),
                    Text("Vaccination Schedule", size=22, weight="bold"),
                ],
            ),
        )

    def build_schedule_list(self, schedules):
        """Build the list of vaccination schedules."""
        controls = []
        current_month = None
        for schedule in schedules:
            if schedule["month"] != current_month:
                current_month = schedule["month"]
                controls.append(
                    Container(
                        content=Text(current_month, size=15, weight="bold", color=ft.colors.BLACK),
                        alignment=ft.alignment.center,  # Center the month text
                    )
                )
                controls.append(Divider(height=5, color="transparent"))
            controls.append(self.create_schedule_container(schedule))
            controls.append(Divider(height=5, color="transparent"))
        return controls

    def create_schedule_container(self, schedule):
        """Create a container for a single vaccination schedule."""
        return Container(
            width=275,
            height=190,
            bgcolor="white10",
            border_radius=11,
            animate=animation.Animation(400, "decelerate"),
            padding=padding.only(left=10, right=10, top=10),
            clip_behavior=ClipBehavior.HARD_EDGE,
            alignment=ft.alignment.center,  # Center the content
            content=Column(
                controls=self.get_vaccine_data(schedule),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center children horizontally
            ),
        )

    def get_vaccine_data(self, schedule):
        """Get the vaccine data for a single schedule."""
        return [
            Row([Icon(name=Icons.LOCAL_HOSPITAL, color="#B4E8F0"), Text(schedule["hospital"])]),
            Row([Icon(name=Icons.LOCATION_PIN, color="RED"), Text(schedule["location"])]),
            Row([Icon(name=Icons.CALENDAR_MONTH, color="blue"), Text(schedule["date"])]),
            Row([Icon(name=Icons.ACCESS_TIME, color="blue"), Text(schedule["time"])]),
            Row([Icon(name=Icons.MEDICATION, color="orange"), Text(schedule["vaccine"])]),
        ]