import flet as ft

def signup_view(page: ft.Page, register_user):
    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    confirm_password_field = ft.TextField(label="Confirm Password", password=True)
    status_text = ft.Text("")

    def on_signup_click(e):
        if password_field.value != confirm_password_field.value:
            status_text.value = "Passwords do not match!"
            status_text.update()
            return
        
        success, message = register_user(username_field.value, password_field.value)
        status_text.value = message
        status_text.update()
        if success:
            page.go("/login")

    def on_login_click(e):
        page.go("/login")

    return ft.View(
        "/signup",
        [
            ft.AppBar(title=ft.Text("Sign Up"), bgcolor=ft.colors.BLUE),
            username_field,
            password_field,
            confirm_password_field,
            ft.ElevatedButton("Sign Up", on_click=on_signup_click),
            status_text,
            ft.TextButton("Already have an account? Login", on_click=on_login_click),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
