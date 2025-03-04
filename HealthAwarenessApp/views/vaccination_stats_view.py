import flet as ft
import requests
import matplotlib
import matplotlib.pyplot as plt

from flet import Text, Container, SearchBar, border, ElevatedButton, View, IconButton, Icons, AppBar, Row, Icon, ImageFit
from flet import CrossAxisAlignment, MainAxisAlignment, Page, Column, ListView, alignment, PopupMenuButton, PopupMenuItem,Image
from flet.matplotlib_chart import MatplotlibChart

# Use the SVG backend for compatibility
matplotlib.use("svg")
API_BASE_URL = "http://127.0.0.1:8000"

class StatsAppBar(AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/"),
            ),leading_width=50,
            title = Text("LifeTrack"),
            actions=[
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Dashboard"),
                        PopupMenuItem(text="Health Articles", on_click = lambda _: page.go("/articles")),
                        PopupMenuItem(text="Health Resources", on_click = lambda _: page.go("/resources")),
                        PopupMenuItem(text="Stats", on_click = lambda _: page.go("/stats")),
                    ]
                ),
                ElevatedButton("My Profile"),
            ]
        )

def create_vaccination_figure(data):
    """
    data is a list of dicts like: [{"date": "2025-03-01", "count": 150}, ...]
    Returns a Matplotlib figure object.
    """
    dates = [item["date"] for item in data]
    counts = [item["count"] for item in data]

    fig, ax = plt.subplots()
    ax.plot(dates, counts, marker='o')
    ax.set_title("Daily Vaccination Counts")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Vaccinations")
    ax.grid(True)
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig

def VaccinationStatsView(page: Page):
    page.title = "Vaccination Statistics"
    page.scroll = True

    # Fetch stats from the API
    response = requests.get(f"{API_BASE_URL}/vaccination-stats")
    if response.status_code == 200:
        stats_data = response.json()
    else:
        stats_data = []

    # Create a Matplotlib figure
    fig = create_vaccination_figure(stats_data)
    
    # Create two separate chart instances (you cannot reuse the same widget)
    chart1 = MatplotlibChart(fig, expand=True)
    chart1.width = 800
    chart1.height = 400

    chart2 = MatplotlibChart(fig, expand=True)
    chart2.width = 800
    chart2.height = 400

    # Wrap your view in a scrollable Column with reduced spacing and no extra margin
    return Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        spacing=10,  # Reduce spacing between children
        controls=[
            Text("Vaccination Statistics", size=20, weight="bold"),
            Row(
                controls=[chart1, chart2],
            ),
            Row(
                controls=[
                    chart1, chart2
                ]
            )
        ]
    )

