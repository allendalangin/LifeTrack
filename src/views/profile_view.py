import flet as ft

class ProfileAppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color="#0cb4cc",
                on_click=lambda e: page.go("/home"),  # Handle back navigation
            ),
            title=ft.Column(
                controls=[ 
                    ft.Container(height=3),
                    ft.Image(
                        src="src/assets/LifeTrackLogo.png",
                        height=55,
                        fit=ft.ImageFit.FIT_HEIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            center_title=True,
            toolbar_height=50,
        )

class ProfileView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.username = page.username  # Fetch username from the page object
        self.update_message = ft.Text("", size=16, weight="bold", color=ft.colors.GREEN_500)  # Message text field

    def build(self):
        """Build and return the profile view."""
        self.username_field = ft.TextField(
            label="New Username",
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
                    self.update_message,  # Add the update message text here
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,  # Center the content
            expand=True,  # Expand to fill the available space
        )

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
            appbar=ProfileAppBar(self.page)
        )

    async def save_username(self, e=None):
        """Save the username."""
        # Get the value from the TextField
        new_username = self.username_field.value.strip()

        # Check if the new username is empty
        if not new_username:
            self.update_message.value = "Username cannot be empty."
            self.update_message.color = ft.colors.RED_500  # Red color for error
            self.page.update()
            return

        # Check if the new username is the same as the current username
        if new_username == self.username:
            self.update_message.value = "The input username is the same as the current username."
            self.update_message.color = ft.colors.RED_500  # Red color for error
            self.page.update()
            return

        # Proceed with the update if the new username is valid
        try:
            # Call the method to update the username in the database
            await self.controller.update_username_in_db(new_username)
            self.update_message.value = "Username updated successfully!"
            self.update_message.color = ft.colors.GREEN_500  # Green color for success
        except Exception as e:
            # Handle any exceptions (e.g., database or API issues)
            self.update_message.value = f"Error: {str(e)}"
            self.update_message.color = ft.colors.RED_500  # Red color for error

        # Update the page to reflect changes
        self.page.update()

