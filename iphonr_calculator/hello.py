import flet
from flet import Page, Column, Container, Text, colors

def main(page: Page):
    page.title = "Hello World"
    page.bgcolor = colors.ORANGE

    container = Container(
        content=Text("Hello Rachit Patel, how are you?"),
        width=300,
        height=300,
    )

    column = Column(
        controls=[container],
        height=300,  # Setting the height for the Column
    )

    page.add(column)

flet.app(target=main)
