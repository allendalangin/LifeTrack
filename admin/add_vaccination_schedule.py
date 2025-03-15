import flet as ft
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Connection
uri = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.vaccination  # Database name
collection = db.vaccination_schedules  # Collection name

def main(page: ft.Page):
    page.title = "Vaccination Schedule Input"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Input fields for vaccination schedule
    month = ft.TextField(label="Month", width=300)
    hospital = ft.TextField(label="Hospital", width=300)
    location = ft.TextField(label="Location", width=300)
    date = ft.TextField(label="Date (YYYY-MM-DD)", width=300)
    time = ft.TextField(label="Time (HH:MM AM/PM)", width=300)
    vaccine = ft.TextField(label="Vaccine", width=300)

    # Function to save data to MongoDB
    def save_data(e):
        data = {
            "month": month.value,
            "hospital": hospital.value,
            "location": location.value,
            "date": date.value,
            "time": time.value,
            "vaccine": vaccine.value
        }

        # Insert into MongoDB
        collection.insert_one(data)
        print("Data saved to MongoDB!")

        # Clear fields after saving
        month.value = ""
        hospital.value = ""
        location.value = ""
        date.value = ""
        time.value = ""
        vaccine.value = ""
        page.update()

    # UI Components
    form = ft.Column(
        [
            month,
            hospital,
            location,
            date,
            time,
            vaccine,
            ft.ElevatedButton("Save", on_click=save_data)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    page.add(form)

# Run the app
ft.app(target=main)
