import flet as ft
from flet import *

#top part
class MainContainer(Container):
    def __init__(self):
        super().__init__(
            Container(
                width=275,
                height=60,
                content = Column(
                    spacing=3,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text(
                            "Health Is Wealth",
                            size=12,
                            weight="W_400",
                            color="white54",
                        ),
                        Text(
                            "Vaccination Schedule",
                            size=22,
                            weight="bold",
                            
                        )
                    ]
                )
            )
        )

class ScheduleContainer(Container):
    def __init__(
        self,
        month : str,
        hospital : str,
        location : str,
        date : str,
        time : str,
        vaccine : str,
    ):
        self.month = month
        self.hospital = hospital
        self.location = location
        self.date = date
        self.time = time
        self.vaccine = vaccine
        super().__init__(
            width=275,
            height=190,
            bgcolor="white10",
            border_radius=11,
            animate=animation.Animation(400, "decelerate"),
            padding=padding.only(left=10, right=10, top=10),
            clip_behavior=ClipBehavior.HARD_EDGE, #clips content if it overflows
            content=Column(
                self.GetVaccineData()
            )
        ) 

    def GetVaccineData(self):

        return[
            Row(
                controls=[
                    Icon(
                        name=Icons.LOCAL_HOSPITAL,  
                        color="#B4E8F0",
                    ),
                    Text(
                        self.hospital,
                    )
                ]
            ),
            Row(
                controls=[
                    Icon(
                        name=Icons.LOCATION_PIN,  
                        color="RED",
                    ),
                    Text(
                        self.location,
                    )
                ]
            ),
            Row(
                controls=[
                    Icon(
                        name=Icons.CALENDAR_MONTH,  
                        color="blue",
                    ),
                    Text(
                        self.date,
                    )
                ]
            ),
            Row(
                controls=[
                    Icon(
                        name=Icons.ACCESS_TIME,  
                        color="blue",
                    ),
                    Text(
                        self.time,
                    )
                ]
            ),
            Row(
                controls=[
                    Icon(
                        name=Icons.MEDICATION,  
                        color="orange",
                    ),
                    Text(
                        self.vaccine,
                    )
                ]
            )
        ]
#HARD CODE MUNA
schedule_data = [
    {"month": "January", "hospital": "Hospital A", "location": "Location A", "date": "Jan 10", "time": "10:00 AM", "vaccine": "Vaccine X"},
    {"month": "January", "hospital": "Hospital B", "location": "Location B", "date": "Jan 20", "time": "2:00 PM", "vaccine": "Vaccine Y"},
    {"month": "February", "hospital": "Hospital C", "location": "Location C", "date": "Feb 05", "time": "9:00 AM", "vaccine": "Vaccine Z"},
    {"month": "February", "hospital": "Hospital D", "location": "Location D", "date": "Feb 18", "time": "11:00 AM", "vaccine": "Vaccine W"},
]           

def build_schedule_list(schedules):
    controls=[]
    current_month = None
    for schedule in schedules:
        if schedule["month"] != current_month:
            current_month = schedule["month"]
            controls.append(
                Text(current_month, size=15, weight="bold", color="white"),
            )
            controls.append(Divider(height=5, color="transparent"))
        controls.append(
            ScheduleContainer(
                schedule["month"],
                schedule["hospital"],
                schedule["location"],
                schedule["date"],
                schedule["time"],
                schedule["vaccine"],
            )
        )
        controls.append(Divider(height=5, color="transparent"))
    return controls

def main(page: Page):
    page.title = "Vaccination Schedules"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    
     # Build the schedule list controls using our helper function
    schedule_controls = build_schedule_list(schedule_data)
    main_container = Container(
        width=1600,
        height=900,
        bgcolor="black",
        border_radius = 40,
        padding = 20,
        content = ListView(
            spacing=10,
            controls=[
                Divider(height=20, color="transparent"),
                MainContainer(),
                Divider(height=0, color="white24"),
            ] + schedule_controls
        )
    )
    
    page.add(main_container)
    pass

if __name__ == "__main__":
    ft.app(main)