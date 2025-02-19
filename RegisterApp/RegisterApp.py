import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column


def registerPage(page: ft.Page)-> None:
    #TIP: Always Setup Page Attributes
    page.title = "Sign Up Form"
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.theme_mode=ft.ThemeMode.DARK
    page.window.width=800
    page.window.height=600
    page.window.resizable=True

    #Setup Controls
    #note: variable: type of control
    username_textfield: TextField = TextField(label = "Username", text_align=ft.TextAlign.LEFT, width=200)
    password_textfield: TextField = TextField(label = "Password", text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox: Checkbox = Checkbox(label = "Agree to Terms & Conditions", value=False)
    signup_button: ElevatedButton = ElevatedButton(text="Sign Up", width=200, disabled=True)
    home_button: ElevatedButton = ElevatedButton(text="HOME",icon=ft.Icons.HOME, icon_color="white")

    #Define Functions
    def isValid(e: ft.ControlEvent)->None:
        if all([username_textfield.value, password_textfield.value, checkbox.value]):
            signup_button.disabled = False
        else:
            signup_button.disabled = True
        
        page.update() #always include update whenever UI changes
    
    def signUp(e: ft.ControlEvent)->None:
        print("Username: " + username_textfield.value)
        print("Password: " + password_textfield.value)

        page.clean()
        page.add(
            ft.Row(
                controls=[
                    ft.Text("Welcome: " + username_textfield.value + "!", size=20)
                ],

                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def goHome(e: ft.ControlEvent)->None:
        page.clean()
        page.add()
    
    #Assign functionality to control
    username_textfield.on_change = isValid
    password_textfield.on_change = isValid
    checkbox.on_change= isValid
    signup_button.on_click = signUp


    #Render Elements

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        username_textfield, password_textfield, checkbox, signup_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    

if __name__ == "__main__":
    ft.app(target=registerPage) 