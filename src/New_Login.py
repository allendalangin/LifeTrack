import flet as ft

def login_view(page: ft.Page, authenticate_user):
    # Define the input fields and buttons
    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    status_text = ft.Text("", color=ft.colors.RED)
    login_button = ft.ElevatedButton("Login", on_click=lambda e: on_login_click(e), width=300)
    signup_button = ft.TextButton("Don't have an account? Sign Up", on_click=lambda e: page.go("/signup"))

    # Login click handler
    def on_login_click(e):
        success, message = authenticate_user(username_field.value, password_field.value)
        status_text.value = message
        status_text.update()
        if success:
            page.go("/home")

    # Create a container for the login form
    login_form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(  # Add logo above "Login"
                    src="src/assets/LifeTrackLogo.png",
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text("Login", size=30, weight="bold", color=ft.colors.BLUE),
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
        bgcolor=ft.colors.WHITE,
        width=400,
        alignment=ft.alignment.center,
    )

    # Create a main container to center the login form
    main_container = ft.Container(
        content=login_form,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.colors.BLUE_100,
    )

    # Return the view with the main container
    return ft.View(
        "/login",
        controls=[main_container],
        padding=0,
        spacing=0,
    )
