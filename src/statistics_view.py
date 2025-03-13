import flet as ft
import matplotlib.pyplot as plt
from pymongo import MongoClient
from io import BytesIO
import base64

# MongoDB Connection
uri = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client.statistics
collection = db.by_year

def fetch_data():
    return list(collection.find())

def plot_data(data):
    plt.figure(figsize=(6, 4))
    plt.plot([p["x"] for p in data["data_points"]], 
             [float(p["y"]) for p in data["data_points"]],
             marker='o', linestyle='-')
    plt.title(data.get("table_title", "Statistics Graph"))
    plt.xlabel(data.get("x_axis_label", "X-Axis"))
    plt.ylabel(data.get("y_axis_label", "Y-Axis"))
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def statistics_view(page):
    data_options = fetch_data()
    dropdown = ft.Dropdown(options=[ft.dropdown.Option(d["table_title"]) for d in data_options])
    image = ft.Image()

    def update_chart(e):
        selected_data = next(d for d in data_options if d["table_title"] == dropdown.value)
        img_data = plot_data(selected_data)
        image.src_base64 = img_data
        image.update()
    
    dropdown.on_change = update_chart
    
    return ft.View(
        "/stats",
        controls=[
            ft.Column([
                ft.Text("Select Data to Display", size=18, weight="bold"),
                dropdown,
                image
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    )
