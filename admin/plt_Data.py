import flet as ft
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI
uri = "mongodb+srv://allendalangin15:Kl9y8WC05MdEVXC5@database.7fqnq.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Database and collection
db = client.test  # Database name
collection = db.statistics  # Collection name

# Fetch all documents from the collection
data = list(collection.find({}))

# Main Flet app
def main(page: ft.Page):
    page.title = "Statistics Graphs"
    page.scroll = "auto"  # Enable scrolling on the page

    # Create a column to hold all the graphs
    graphs_column = ft.Column(scroll="auto", expand=True)

    # Iterate through each document and create a graph
    for document in data:
        table_title = document['table_title']
        x_axis_label = document['x_axis_label']
        y_axis_label = document['y_axis_label']
        data_points = document['data_points']

        # Prepare data for the chart
        x_values = [point['x'] for point in data_points]
        y_values = [int(point['y']) for point in data_points]  # Convert y values to integers

        # Create a line chart
        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=[
                        ft.LineChartDataPoint(i, y_values[i]) for i in range(len(x_values))
                    ],
                    stroke_width=2,
                    color=ft.colors.BLUE,  # Use deprecated colors enum
                    curved=True,
                ),
            ],
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=y_values[i],
                        label=ft.Text(str(y_values[i])),
                    ) for i in range(len(y_values))
                ],
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Text(x_values[i]),
                    ) for i in range(len(x_values))
                ],
                labels_size=40,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),  # Use deprecated with_opacity
            expand=True,
        )

        # Add the chart to the column
        graphs_column.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(table_title, size=18, weight="bold"),
                        ft.Text(f"X-Axis: {x_axis_label}", size=14),
                        ft.Text(f"Y-Axis: {y_axis_label}", size=14),
                        chart,
                    ],
                    spacing=10,
                ),
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),  # Use deprecated colors enum
                border_radius=5,
                margin=ft.margin.symmetric(vertical=5),
            )
        )

    # Add the column to the page
    page.add(graphs_column)

# Run the Flet app
ft.app(target=main)