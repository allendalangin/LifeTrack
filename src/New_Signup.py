import flet as ft

def signup_view(page: ft.Page, register_user):
    # Define input fields and buttons
    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    confirm_password_field = ft.TextField(label="Confirm Password", password=True, width=300)
    status_text = ft.Text("", color=ft.colors.RED)
    signup_button = ft.ElevatedButton("Sign Up", on_click=lambda e: on_signup_click(e), width=300)
    login_button = ft.TextButton("Already have an account? Login", on_click=lambda e: page.go("/login"))

    # Signup click handler
    def on_signup_click(e):
        if password_field.value != confirm_password_field.value:
            status_text.value = "Passwords do not match!"
            status_text.update()
            return

        success, message = register_user(username_field.value, password_field.value)
        status_text.value = message
        status_text.color = ft.colors.GREEN if success else ft.colors.RED
        status_text.update()
        if success:
            page.go("/login")

    # Create a container for the signup form
    signup_form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(  # Add logo above "Sign Up"
                    src="src/assets/LifeTrackLogo.png",
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text("Sign Up", size=30, weight="bold", color=ft.colors.BLUE),
                username_field,
                password_field,
                confirm_password_field,
                signup_button,
                status_text,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=20,
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        width=400,
        alignment=ft.alignment.center,
    )

    # Create a main container to center the signup form
    main_container = ft.Container(
        content=signup_form,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.colors.BLUE_100,
    )

    # Return the view with the main container
    return ft.View(
        "/signup",
        controls=[main_container],
        padding=0,
        spacing=0,
    )
