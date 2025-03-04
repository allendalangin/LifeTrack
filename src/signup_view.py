import flet as ft

def signup_view(page: ft.Page):
    def on_signup_click(e):
        # Signup logic
        page.go("/home")

    def on_login_click(e):
        page.go("/login")

    return ft.View(
        "/signup",
        [
            ft.AppBar(title=ft.Text("Sign Up"), bgcolor=ft.colors.BLUE),
            ft.TextField(label="Username"),
            ft.TextField(label="Password", password=True),
            ft.TextField(label="Confirm Password", password=True),
            ft.ElevatedButton("Sign Up", on_click=on_signup_click),
            ft.TextButton("Already have an account? Login", on_click=on_login_click),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )