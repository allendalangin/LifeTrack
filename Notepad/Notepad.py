import flet as ft
from flet import Row, Column, Text, MainAxisAlignment, CrossAxisAlignment, Page, InputBorder,ControlEvent

class TextEditor(ft.TextField):
    def __init__(self)->None:
        super().__init__(
            multiline=True,
            autofocus=True,
            border=InputBorder.NONE,
            border_radius=0,
            border_width=0,
            min_lines=40,
            on_change=self.SaveText,
            content_padding=30,
            cursor_color="yellow",
        )
    
        self.value = self.ReadText()
        

    def SaveText(self, e: ControlEvent)->None:
        with open("save.txt", "w") as f:
            f.write(self.value)

    def ReadText(self)->str | None:
        try:
            with open("save.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            self.hint_text="Welcome to text editor..."


def main(page: Page)->None:
    page.title = "Ket Notepad"
    page.scroll = True
    page.theme_mode = "dark"
    page.add(TextEditor())

if __name__ == "__main__":
    ft.app(main)