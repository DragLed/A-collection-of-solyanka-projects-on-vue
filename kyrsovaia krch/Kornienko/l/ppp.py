import flet



def main(page: flet.Page):
    page.title = "Login"
    page.bgcolor = flet.colors.BLUE_GREY_500
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    def route_changer(e: flet.RouteChangeEvent):
        page.views.clear()
        login.btn.on_click = lambda _: page.go("/second")

        page.views.append(
            flet.View(
                route="/",
                controls=[
                    login
                ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                vertical_alignment=flet.MainAxisAlignment.CENTER
            )
        )

        if page.route == "/second":
            page.views.append(
                flet.View(
                    route="/second",
                    controls=[
                        flet.Text(
                            "Second page",
                            size=150,
                            style=flet.FontWeight.BOLD
                        ),
                        flet.TextButton(
                            text="Go back",
                            on_click=lambda _: page.go("/")
                        )
                    ]
                )
            )

        page.update()

    page.on_route_change = route_changer
    page.go(page.route)

if __name__ == "__main__":
    flet.app(main)