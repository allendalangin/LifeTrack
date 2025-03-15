import flet as ft
from flet import *
from src.controllers.vaccination_schedule_controller import VaccinationScheduleController

class VaccinationScheduleView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = VaccinationScheduleController()

    def build(self):
        """Build the vaccination schedule view."""
        schedule_data = self.controller.fetch_schedules()
        schedule_controls = self.build_schedule_list(schedule_data)

        main_container = Container(
            width=1600,
            height=900,
            border_radius=40,
            padding=20,
            content=ListView(
                spacing=10,
                controls=[
                    Divider(height=20, color="transparent"),
                    self.create_main_container(),
                    Divider(height=0, color="white24"),
                ]
                + schedule_controls,
            ),
        )

        return main_container

    def create_main_container(self):
        """Create the main container for the vaccination schedule view."""
        return Container(
            width=275,
            height=60,
            content=Column(
                spacing=3,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text("Health Is Wealth", size=12, weight="W_400", color="white54"),
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
                controls.append(Text(current_month, size=15, weight="bold", color="white"))
                controls.append(Divider(height=5, color="transparent"))
            controls.append(
                self.create_schedule_container(schedule)
            )
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
            content=Column(self.get_vaccine_data(schedule)),
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