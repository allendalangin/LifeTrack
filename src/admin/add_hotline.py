import flet as ft
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection string
MONGO_URI = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
def connect_to_mongodb():
    try:
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        client.admin.command('ping')  # Test connection
        print("Connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

# Save data to MongoDB
def save_to_mongodb(data):
    client = connect_to_mongodb()
    if client:
        db = client.health_resources  # Database name
        collection = db.hotline  # Collection name
        try:
            collection.insert_one(data)
            print("Data saved to MongoDB!")
        except Exception as e:
            print(f"Failed to save data: {e}")
    else:
        print("Could not connect to MongoDB.")

# Main Flet app
def main(page: ft.Page):
    page.title = "Health Resources Hotline Form"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Text fields
    department_name = ft.TextField(label="Department Name", width=400)
    phone_number = ft.TextField(label="Phone Number", width=400)
    telephone_number = ft.TextField(label="Telephone Number", width=400)
    email = ft.TextField(label="Email", width=400)

    # Submit button
    def submit_form(e):
        data = {
            "department_name": department_name.value,
            "phone_number": phone_number.value,
            "telephone_number": telephone_number.value,
            "email": email.value,
        }
        save_to_mongodb(data)
        page.snack_bar = ft.SnackBar(ft.Text("Data saved successfully!"))
        page.snack_bar.open = True
        page.update()

    submit_button = ft.ElevatedButton(text="Submit", on_click=submit_form)

    # Add controls to the page
    page.add(
        ft.Column(
            [
                ft.Text("Health Resources Hotline Form", size=24, weight="bold"),
                department_name,
                phone_number,
                telephone_number,
                email,
                submit_button,
            ],
            spacing=20,
        )
    )

# Run the app
ft.app(target=main)