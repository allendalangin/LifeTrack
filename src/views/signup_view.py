# src/views/signup_view.py

import flet as ft

class SignupView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.custom_color = "#0cb4cc"

    def build(self):
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.update()

        self.username_field = ft.TextField(
            label="Username", 
            width=300,
            bgcolor=ft.colors.WHITE,
            color=self.custom_color,
            border_color=self.custom_color,
            border_width=1,
            border_radius=10,
            label_style=ft.TextStyle(color=self.custom_color),
        )
        self.password_field = ft.TextField(
            label="Password", 
            password=True, 
            width=300,
            bgcolor=ft.colors.WHITE,
            color=self.custom_color,
            border_color=self.custom_color,
            border_width=1,
            border_radius=10,
            label_style=ft.TextStyle(color=self.custom_color),
        )
        self.confirm_password_field = ft.TextField(
            label="Confirm Password", 
            password=True, 
            width=300,
            bgcolor=ft.colors.WHITE,
            color=self.custom_color,
            border_color=self.custom_color,
            border_width=1,
            border_radius=10,
            label_style=ft.TextStyle(color=self.custom_color),
        )
        self.status_text = ft.Text("", color=ft.colors.RED)
        self.signup_button = ft.ElevatedButton(
            "Sign Up", 
            on_click=self.on_signup_click, 
            width=300,
            color=self.custom_color,
        )
        self.login_button = ft.TextButton(
            "Already have an account? Login", 
            on_click=lambda e: self.page.go("/login"),
            style=ft.ButtonStyle(color=self.custom_color),
        )

        signup_form = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(
                        src="src/assets/LifeTrackLogo.png",
                        height=200,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text("Sign Up", size=30, weight="bold", color=self.custom_color),
                    self.username_field,
                    self.password_field,
                    self.confirm_password_field,
                    self.signup_button,
                    self.status_text,
                    self.login_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.WHITE),
            image_src="src/assets/AuthBackground.jpg",
            image_fit=ft.ImageFit.COVER,
            expand=True,
            alignment=ft.alignment.center,
        )

        main_container = ft.Container(
            content=signup_form,
            alignment=ft.alignment.center,
            expand=True,
        )

        return ft.View(
            "/signup",
            controls=[main_container],
            padding=0,
            spacing=0,
        )

    async def on_signup_click(self, e):
        username = self.username_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value
        await self.controller.handle_signup(username, password, confirm_password)

    def update_status(self, message, is_success):
        self.status_text.value = message
        self.status_text.color = ft.colors.GREEN if is_success else ft.colors.RED
        self.status_text.update()

    def navigate_to_login(self):
        self.page.go("/login")