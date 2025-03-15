import flet as ft
from flet import *
from src.controllers.vaccination_schedule_controller import VaccinationScheduleController

# Top part
class MainContainer(Container):
    def __init__(self):
        super().__init__(
            Container(
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
        )

class ScheduleContainer(Container):
    def __init__(self, month, hospital, location, date, time, vaccine):
        super().__init__(
            width=275,
            height=190,
            bgcolor="white10",
            border_radius=11,
            animate=animation.Animation(400, "decelerate"),
            padding=padding.only(left=10, right=10, top=10),
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Column(self.GetVaccineData(month, hospital, location, date, time, vaccine)),
        )

    def GetVaccineData(self, hospital, location, date, time, vaccine):
        return [
            Row([Icon(name=Icons.LOCAL_HOSPITAL, color="#B4E8F0"), Text(hospital)]),
            Row([Icon(name=Icons.LOCATION_PIN, color="RED"), Text(location)]),
            Row([Icon(name=Icons.CALENDAR_MONTH, color="blue"), Text(date)]),
            Row([Icon(name=Icons.ACCESS_TIME, color="blue"), Text(time)]),
            Row([Icon(name=Icons.MEDICATION, color="orange"), Text(vaccine)]),
        ]

def build_schedule_list(schedules):
    controls = []
    current_month = None
    for schedule in schedules:
        if schedule["month"] != current_month:
            current_month = schedule["month"]
            controls.append(Text(current_month, size=15, weight="bold", color="white"))
            controls.append(Divider(height=5, color="transparent"))
        controls.append(
            ScheduleContainer(schedule["month"], schedule["hospital"], schedule["location"], schedule["date"], schedule["time"], schedule["vaccine"])
        )
        controls.append(Divider(height=5, color="transparent"))
    return controls

def main(page: Page):
    page.title = "Vaccination Schedules"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Fetch data from API
    schedule_data = VaccinationScheduleController.fetch_schedules()

    # Build the schedule list controls dynamically
    schedule_controls = build_schedule_list(schedule_data)

    main_container = Container(
        width=1600,
        height=900,
        bgcolor="black",
        border_radius=40,
        padding=20,
        content=ListView(
            spacing=10,
            controls=[
                Divider(height=20, color="transparent"),
                MainContainer(),
                Divider(height=0, color="white24"),
            ]
            + schedule_controls,
        ),
    )

    page.add(main_container)

if __name__ == "__main__":
    ft.app(main)
