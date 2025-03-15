class DashboardController:
    def __init__(self, view, weather_controller):
        self.view = view
        self.weather_controller = weather_controller

    async def load_weather_data(self):
        """Fetch weather data and update the view."""
        weather_data = await self.weather_controller.fetch_weather_data()
        if weather_data:
            self.view.update_weather_ui(weather_data)

    def handle_navigation(self, destination):
        """Handle navigation to the specified destination."""
        self.view.navigate_to(destination)