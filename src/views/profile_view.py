import flet as ft

class ProfileView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.username = page.username  # Fetch username from the page object

    def build(self):
        """Build and return the profile view."""
        self.username_field = ft.TextField(
            value=self.username,
            label="Username",
            width=300,
        )
        self.save_button = ft.ElevatedButton(
            text="Save",
            on_click=self.save_username,
        )

        # Create a background image
        background_image = ft.Image(
            src="/src/assets/AuthBackground.jpg",  
            fit=ft.ImageFit.COVER,  # Cover the entire window
            opacity=0.8,  # Adjust opacity if needed
        )

        # Wrap the content in a Container with the background image
        content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Edit Profile", size=20, weight="bold"),
                    self.username_field,
                    self.save_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,  # Center the content
            expand=True,  # Expand to fill the available space
        )

        # Overlay the content on top of the background image
        return ft.View(
            "/profile",
            controls=[
                ft.Stack(
                    controls=[
                        background_image,  # Background image
                        content,  # Content on top of the background
                    ],
                    expand=True,  # Expand to fill the window
                )
            ],
            appbar=ft.AppBar(
                title=ft.Text("Profile"),
                center_title=True,
            ),
        )

    async def save_username(self, e):
        """Save the updated username to MongoDB."""
        new_username = self.username_field.value
        if new_username:
            await self.controller.update_username(new_username)  # Call the controller method
            self.page.username = new_username  # Update the username in the page object
            self.page.go("/home")  # Navigate back to the home view