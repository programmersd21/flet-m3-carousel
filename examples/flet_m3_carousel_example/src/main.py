import flet as ft

from flet_m3_carousel import M3Carousel, M3CarouselItem, M3CarouselTapEvent


def main(page: ft.Page) -> None:
    page.title = "M3 Carousel Demo"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def on_tap(event: M3CarouselTapEvent) -> None:
        snack = ft.SnackBar(content=ft.Text(f"Tapped item {event.index}: {event.item_key}"))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    items = [
        M3CarouselItem(
            key=f"item-{index}",
            image=f"https://picsum.photos/seed/m3-{index}/480/320",
            title=f"Item {index}",
            subtitle="M3 carousel",
            prefix_text=f"{index + 1}",
            scrim="gradient",
        )
        for index in range(10)
    ]

    page.add(
        ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Material 3 Carousel", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Scroll or swipe to explore",
                        size=14,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        width=760,
                        height=360,
                        border_radius=20,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=M3Carousel(
                            width=760,
                            height=360,
                            layout="hero",
                            axis="horizontal",
                            hero_alignment="center",
                            free_scroll=True,
                            items=items,
                            on_tap=on_tap,
                        ),
                    ),
                ],
            ),
        )
    )


ft.run(main)
