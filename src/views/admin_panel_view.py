import flet as ft
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# MongoDB connection string
MONGO_URI = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Cloudinary Configuration
cloudinary.config( 
    cloud_name="dp8qhz9w7", 
    api_key="348841966416776", 
    api_secret="G5OouVnntHO5wSz6WpijFjHjGRc", 
    secure=True
)

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
def save_to_mongodb(data, db_name, collection_name):
    client = connect_to_mongodb()
    if client:
        db = client[db_name]
        collection = db[collection_name]
        try:
            collection.insert_one(data)
            print("Data saved to MongoDB!")
        except Exception as e:
            print(f"Failed to save data: {e}")
    else:
        print("Could not connect to MongoDB.")

class AdminPanelView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "LifeTrack Admin Panel"
        self.page.window_width = 1200
        self.page.window_height = 600

        # Logout button
        logout_button = ft.ElevatedButton(
            "Logout",
            icon=ft.icons.LOGOUT,
            on_click=lambda e: page.go("/login"),  # Navigate to login page
        )

        # Container for dynamic content
        background_image = ft.Image(
            src="src/assets/AuthBackground.jpg",
            fit=ft.ImageFit.COVER,
            width=page.window_width,
            height=page.window_height,
        )

        # Container for dynamic content
        self.content_container = ft.Container(content=ft.Text("Welcome to LifeTrack Admin Panel"), padding=20)

        # Sidebar
        sidebar = ft.Column(
            controls=[
                ft.ElevatedButton("Statistics", data="statistics", on_click=self.switch_view),
                ft.ElevatedButton("Health Resources", data="resources", on_click=self.switch_view),
                ft.ElevatedButton("Vaccination Schedule", data="vaccination", on_click=self.switch_view),
                ft.ElevatedButton("Infographics", data="infographics", on_click=self.switch_view),
            ],
        )

        # Main layout with Stack
        self.layout = ft.Stack(
            [
                background_image,  # Background at the bottom layer
                ft.Column(  # Content above the background
                    [
                        ft.Row([logout_button], alignment="end"),  # Logout button at the top-right
                        ft.Row([sidebar, self.content_container], expand=True),  # Main content below the logout button
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    def switch_view(self, e):
        view = e.control.data

        if view == "statistics":
            self.content_container.content = self.statistics_form()
        elif view == "resources":
            self.content_container.content = self.health_resources_form()
        elif view == "vaccination":
            self.content_container.content = self.vaccination_form()
        elif view == "infographics":
            self.content_container.content = self.infographic_upload_form()

        self.page.update()

    def statistics_form(self):
        table_title = ft.TextField(label="Table Title", width=300)
        x_axis_label = ft.TextField(label="X Axis Label", width=300)
        y_axis_label = ft.TextField(label="Y Axis Label", width=300)

        pairs_container = ft.Column()

        def add_pair(e):
            x_value = ft.TextField(label="X Value", width=200)
            y_value = ft.TextField(label="Y Value", width=200)

            def delete_pair(e):
                pairs_container.controls.remove(row)
                self.page.update()

            minus_button = ft.IconButton(icon=ft.icons.REMOVE_CIRCLE_OUTLINE, icon_color="red", on_click=delete_pair)
            row = ft.Row([x_value, y_value, minus_button])
            pairs_container.controls.append(row)
            self.page.update()

        def save_data(e):
            data = {
                "table_title": table_title.value,
                "x_axis_label": x_axis_label.value,
                "y_axis_label": y_axis_label.value,
                "data_points": []
            }

            for row in pairs_container.controls:
                x = row.controls[0].value
                y = row.controls[1].value
                if x and y:
                    data["data_points"].append({"x": x, "y": y})

            save_to_mongodb(data, "statistics", "by_year")

            table_title.value = ""
            x_axis_label.value = ""
            y_axis_label.value = ""
            pairs_container.controls.clear()
            self.page.update()

        return ft.Column(
            [
                ft.Text("Statistics Input Form", size=24, weight="bold"),
                table_title,
                x_axis_label,
                y_axis_label,
                ft.ElevatedButton("Add X-Y Pair", on_click=add_pair),
                pairs_container,
                ft.ElevatedButton("Save", on_click=save_data)
            ],
            spacing=20
        )

    def vaccination_form(self):
        month = ft.TextField(label="Month", width=300)
        hospital = ft.TextField(label="Hospital", width=300)
        location = ft.TextField(label="Location", width=300)
        date = ft.TextField(label="Date (YYYY-MM-DD)", width=300)
        time = ft.TextField(label="Time (HH:MM AM/PM)", width=300)
        vaccine = ft.TextField(label="Vaccine", width=300)

        def save_data(e):
            data = {
                "month": month.value,
                "hospital": hospital.value,
                "location": location.value,
                "date": date.value,
                "time": time.value,
                "vaccine": vaccine.value
            }

            save_to_mongodb(data, "vaccination", "vaccination_schedules")

            month.value = ""
            hospital.value = ""
            location.value = ""
            date.value = ""
            time.value = ""
            vaccine.value = ""
            self.page.update()

        return ft.Column(
            [
                ft.Text("Vaccination Schedule Input", size=24, weight="bold"),
                month,
                hospital,
                location,
                date,
                time,
                vaccine,
                ft.ElevatedButton("Save", on_click=save_data)
            ],
            spacing=10
        )

    def health_resources_form(self):
        department_name = ft.TextField(label="Department Name", width=400)
        phone_number = ft.TextField(label="Phone Number", width=400)
        telephone_number = ft.TextField(label="Telephone Number", width=400)
        email = ft.TextField(label="Email", width=400)

        def submit_form(e):
            data = {
                "department_name": department_name.value,
                "phone_number": phone_number.value,
                "telephone_number": telephone_number.value,
                "email": email.value,
            }
            save_to_mongodb(data, "health_resources", "hotline")
            self.page.snack_bar = ft.SnackBar(ft.Text("Data saved successfully!"))
            self.page.snack_bar.open = True
            self.page.update()

        return ft.Column(
            [
                ft.Text("Health Resources Hotline Form", size=24, weight="bold"),
                department_name,
                phone_number,
                telephone_number,
                email,
                ft.ElevatedButton("Submit", on_click=submit_form),
            ],
            spacing=20
        )

    def infographic_upload_form(self):
        status_text = ft.Text("", color="green")
        image_display = ft.Image(visible=False, width=400)

        def upload_image(file_path):
            try:
                # Upload image to Cloudinary
                upload_result = cloudinary.uploader.upload(file_path)
                image_url = upload_result["secure_url"]

                # Optimize delivery
                optimized_url, _ = cloudinary_url(upload_result["public_id"], fetch_format="auto", quality="auto")

                # Save URL to MongoDB
                save_to_mongodb({"image_url": optimized_url}, "infographics", "uploads")

                status_text.value = "Upload Successful!"
                image_display.src = optimized_url  # Display the uploaded image
                image_display.visible = True

            except Exception as e:
                status_text.value = f"Upload Failed: {str(e)}"
            
            status_text.update()
            image_display.update()

        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                status_text.value = "Uploading..."
                status_text.update()
                upload_image(file_path)

        file_picker = ft.FilePicker(on_result=pick_files_result)

        return ft.Column(
            [
                ft.Text("Upload Infographic", size=24, weight="bold"),
                ft.ElevatedButton("Choose Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                file_picker,
                status_text,
                image_display,
            ],
            spacing=20
        )

    def build(self):
        # Wrap the layout in a Container and set expand=True
        return ft.View(
            route="/admin",
            controls=[
                ft.Container(
                    content=self.layout,
                    expand=True,  # Expand the container to fill the View
                ),
            ],
        )