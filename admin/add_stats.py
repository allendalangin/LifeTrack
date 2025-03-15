import flet as ft
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Connection
uri = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.statistics # Database name
collection = db.by_year  # Collection name

def main(page: ft.Page):
    page.title = "Statistics Input App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO  # Enable scrolling for the entire page

    # Input fields for table title, x-axis, and y-axis
    table_title = ft.TextField(label="Table Title", width=300)
    x_axis_label = ft.TextField(label="X Axis Label", width=300)
    y_axis_label = ft.TextField(label="Y Axis Label", width=300)

    # Container to hold dynamic x-y pairs
    pairs_container = ft.Column()

    # Function to add a new pair of x and y input fields
    def add_pair(e):
        x_value = ft.TextField(label="X Value", width=200)
        y_value = ft.TextField(label="Y Value", width=200)
        
        # Minus button to delete the pair
        def delete_pair(e):
            pairs_container.controls.remove(row)
            page.update()

        minus_button = ft.IconButton(
            icon=ft.icons.REMOVE_CIRCLE_OUTLINE,
            icon_color="red",
            on_click=delete_pair
        )

        # Create a row with x, y, and minus button
        row = ft.Row([x_value, y_value, minus_button])
        pairs_container.controls.append(row)
        page.update()

    # Function to save data to MongoDB
    def save_data(e):
        # Prepare data to save
        data = {
            "table_title": table_title.value,
            "x_axis_label": x_axis_label.value,
            "y_axis_label": y_axis_label.value,
            "data_points": []
        }

        # Collect x and y values
        for row in pairs_container.controls:
            x = row.controls[0].value
            y = row.controls[1].value
            if x and y:  # Only save if both fields have values
                data["data_points"].append({"x": x, "y": y})

        # Insert data into MongoDB
        collection.insert_one(data)
        print("Data saved to MongoDB!")

        # Clear input fields
        table_title.value = ""
        x_axis_label.value = ""
        y_axis_label.value = ""
        pairs_container.controls.clear()
        page.update()

    # Main content wrapped in a ListView for scrolling
    main_content = ft.ListView(
        expand=True,  # Ensure it takes up available space
        controls=[
            ft.Column(
                [
                    table_title,
                    x_axis_label,
                    y_axis_label,
                    ft.ElevatedButton("Add X-Y Pair", on_click=add_pair),
                    pairs_container,
                    ft.ElevatedButton("Save", on_click=save_data)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20  # Add spacing between controls
            )
        ]
    )

    # Add the main content to the page
    page.add(main_content)

# Run the app
ft.app(target=main)