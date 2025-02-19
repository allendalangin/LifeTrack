import flet as ft
from flet import TextField

def main(page: ft.Page)-> None:
    page.title = "Increment Counter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "dark"
    #page.scroll = "adaptive"

    text_number:TextField = TextField("0", text_align=ft.TextAlign.CENTER, width=50)

    def decrement(e: ft.ControlEvent)-> None:
        text_number.value = str(int(text_number.value)-1)
        page.update()
    
    def increment(e: ft.ControlEvent)-> None:
        text_number.value = str(int(text_number.value)+1)
        page.update()
    
    
    page.add(
        ft.Column(
            controls=[
                ft.Text("Increment/Decrement", size=20, color="green"),
                ft.Row(
                    controls=[
                        ft.IconButton(ft.icons.REMOVE, on_click = decrement),
                        text_number,
                        ft.IconButton(ft.icons.ADD, on_click=increment),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)