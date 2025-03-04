import flet as ft

def login_view(page: ft.Page):
    def on_login_click(e):
        #Login logic
        page.go("/home")

    def on_signup_click(e):
        page.go("/signup")

    return ft.View(
        "/login",
        [
            ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.BLUE),
            ft.TextField(label="Username"),
            ft.TextField(label="Password", password=True),
            ft.ElevatedButton("Login", on_click=on_login_click),
            ft.TextButton("Don't have an account? Sign Up", on_click=on_signup_click),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )