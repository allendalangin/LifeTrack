import flet as ft

def login_view(page: ft.Page, authenticate_user):
    page.window.width = 1200  # Set initial width to 1200 pixels
    page.window.height = 800  # Set initial height to 800 pixels
    page.update()

    # Define the custom text color
    custom_color = "#0cb4cc"

    # Define the input fields and buttons
    username_field = ft.TextField(
        label="Username", 
        width=300,
        bgcolor=ft.colors.WHITE,  # Set white background
        color=custom_color,       # Set text color to #0cc0df
        border_color=custom_color,  # Set border color to #0cc0df
        border_width=1,            # Set border width
        border_radius=10,          # Add rounded corners
        label_style=ft.TextStyle(color=custom_color),
    )
    password_field = ft.TextField(
        label="Password", 
        password=True, 
        width=300,
        bgcolor=ft.colors.WHITE,  # Set white background
        color=custom_color,       # Set text color to #0cc0df
        border_color=custom_color,  # Set border color to #0cc0df
        border_width=1,            # Set border width
        border_radius=10,          # Add rounded corners
        label_style=ft.TextStyle(color=custom_color),
    )
    status_text = ft.Text("", color=ft.colors.RED)
    login_button = ft.ElevatedButton(
        "Login", 
        on_click=lambda e: on_login_click(e), 
        width=300,
        color=custom_color,  # Set text color to #0cc0df
    )
    signup_button = ft.TextButton(
        "Don't have an account? Sign Up", 
        on_click=lambda e: page.go("/signup"),
        style=ft.ButtonStyle(color=custom_color),  # Set text color to #0cc0df
    )

    # Login click handler
    def on_login_click(e):
        success, message, username = authenticate_user(username_field.value, password_field.value)
        status_text.value = message
        status_text.update()
        if success:
            page.go(f"/home?username={username}")

    # Create a container for the login form with an image background
    login_form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(  # Add logo above "Login"
                    src="src/assets/LifeTrackLogo.png",
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text("Login", size=30, weight="bold", color=custom_color),  # Set text color to #0cc0df
                username_field,
                password_field,
                login_button,
                status_text,
                signup_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=20,
        border_radius=10,
        bgcolor=ft.colors.with_opacity(0.7, ft.colors.WHITE),  # Semi-transparent background
        image_src="src/assets/AuthBackground.jpg",  # Set the image background
        image_fit=ft.ImageFit.COVER,  # Ensure the image covers the container
        expand=True,  # Make the login form expand to fill the available width
        alignment=ft.alignment.center,
    )

    # Create a main container to center the login form
    main_container = ft.Container(
        content=login_form,
        alignment=ft.alignment.center,
        expand=True,  # Make the main container expand to fill the page
    )

    # Return the view with the main container
    return ft.View(
        "/login",
        controls=[main_container],
        padding=0,
        spacing=0,
    )