import flet as ft
from flet import Page, Row, Text, KeyboardEvent, Column

def main(page: ft.Page)->None:
    page.title="Keyboard Pro"
    page.spacing=30
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.theme_mode="dark"

    #create views
    key: Text = Text("Key", size=30)
    shift: Text = Text("Shift", size=30, color = "red")
    ctrl: Text = Text("Ctrl", size=30, color = "blue")
    alt: Text = Text("Alt", size=30, color = "yellow")
    win: Text = Text("Win", size=30, color = "green")

    #keyboard events

    def onKeyboard(e: KeyboardEvent)->None:
        key.value = e.key
        shift.visible = e.shift
        ctrl.visible = e.ctrl
        alt.visible = e.alt
        win.visible = e.meta
        print(e.data)
        page.update()
    
    

    #link keeb to page
    page.on_keyboard_event = onKeyboard

    #render page
    page.add(
        ft.Text("Press any key...", size=20),
        Row(
            controls=[
                key, shift, ctrl, alt, win,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)