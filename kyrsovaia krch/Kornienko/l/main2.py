import flet as ft




class LLogin(ft.UserControl):


    btn = ft.ElevatedButton(
        text="На другую страницу",
        width=500,
        height=75
    )


    def build(self):
        return ft.Container(
            width=600,
            height=600,
            bgcolor="red",
            border_radius=90,
            content=ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.btn
                ]
            )
        )
