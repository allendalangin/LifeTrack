import flet as ft

def home_view(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    def on_logout_click(e):
        # Back to login
        page.go("/login")

    # Logout
    appbar = ft.AppBar(
        title=ft.Text("Home"),
        bgcolor=ft.colors.BLUE,
        actions=[
            ft.IconButton(icon=ft.icons.LOGOUT, on_click=on_logout_click),
        ],
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )

    return ft.View(
        "/home",
        [
            appbar,
            ft.SafeArea(
                ft.Container(
                    counter,
                    alignment=ft.alignment.center,
                ),
                expand=True,
            ),
        ],
    )