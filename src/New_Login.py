import flet as ft

def login_view(page: ft.Page, authenticate_user):
    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    status_text = ft.Text("")

    def on_login_click(e):
        success, message = authenticate_user(username_field.value, password_field.value)
        status_text.value = message
        status_text.update()
        if success:
            page.go("/home")

    def on_signup_click(e):
        page.go("/signup")

    return ft.View(
        "/login",
        [
            ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.BLUE),
            username_field,
            password_field,
            ft.ElevatedButton("Login", on_click=on_login_click),
            status_text,
            ft.TextButton("Don't have an account? Sign Up", on_click=on_signup_click),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
