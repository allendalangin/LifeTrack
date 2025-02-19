import flet as ft
from flet import Row, Column, Text, ElevatedButton, ControlEvent, MainAxisAlignment

class IncrementCounter(ft.Row):
    #initialize the thing
    def __init__(self, text: str, start_number: int = 0)->None:
        super().__init__()
        #constructor
        self.text = text
        self.counter = start_number
        self.text_number: Text = Text(value=str(start_number),size=40)

        #render the things needed
        self.controls=[
            ElevatedButton(text=self.text, on_click=self.increment), 
            self.text_number
        ]
        #alignment stuff
        self.vertical_alignment=MainAxisAlignment.CENTER
        self.alignment=MainAxisAlignment.CENTER


    def increment(self,e: ControlEvent)->None:
        self.counter += 1
        self.text_number.value = str(self.counter)
        self.update()


def main(page: ft.Page)->None:
    page.title = "Reusable Controls"
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    #3 Increment Counters
    page.add(IncrementCounter("People"))
    page.add(IncrementCounter("Dogs"))
    page.add(IncrementCounter("Again"))
    page.add(IncrementCounter("Niggers in my yard"))

if __name__ == "__main__":
    ft.app(target=main)