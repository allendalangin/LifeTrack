import flet as ft
from login_view import login_view
from signup_view import signup_view
from home_view import home_view

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/signup":
            page.views.append(signup_view(page))
        elif page.route == "/home":
            page.views.append(home_view(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.max_width = 600
    page.max_height = 600
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main)