"""Health Resources UI"""

import flet as ft
import asyncio

# Component for displaying the search results area
class SearchResult(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        col={"xs": 12, "sm": 12, "lg": 12, "xl": 11},
        alignment=ft.alignment.center,
    ):
        super().__init__(col=col, alignment=alignment)
        self.page = page
        self.height = self.page.height

# Main Article component
class Article(ft.Container):
    def __init__(
        self,
        article,
        col={"xs": 12, "sm": 12, "lg": 12, "xl": 11},
        expand=True,
    ):
        super().__init__(col=col, expand=expand)
        self.article = article

        self.inputQuery = ft.TextField(
            border_color="transparent",
            height=50,
            color="white",
            hint_text="Type to search resources...",
            on_submit=lambda e: asyncio.run(self.run_compilation(e)),
        )

        self.loader = ft.ProgressBar(
            value=0,
            bar_height=1.25,
            bgcolor="transparent",
            color="#64b687",
        )

        self.grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=350,
            child_aspect_ratio=1,
            spacing=45,
            run_spacing=45,
        )

        self.column = ft.Column(
            horizontal_alignment="center",
            spacing=0,
            controls=[
                ft.Divider(height=20, color="transparent"),
                ft.Container(
                    content=ft.Row(
                        spacing=4,
                        alignment="center",
                        controls=[
                            # Title section
                            ft.Column(
                                alignment="center",
                                horizontal_alignment="start",
                                controls=[
                                    ft.Text(
                                        "Health Resources",
                                        style=ft.TextThemeStyle("headlineMedium"),
                                        weight="bold",
                                        color="white",
                                    )
                                ],
                            ),
                            ft.Column(
                                alignment="center",
                                horizontal_alignment="start",
                                controls=[
                                    ft.Text(
                                        "",
                                        style=ft.TextThemeStyle("headlineMedium"),
                                        weight="bold",
                                        color="white",
                                    )
                                ],
                            ),
                        ],
                    )
                ),
                ft.Divider(height=20, color="transparent"),
                # Text field container
                ft.Container(
                    content=self.inputQuery,
                    height=50,
                    border=ft.border.all(1, "#64b687"),
                    border_radius=6,
                    shadow=ft.BoxShadow(
                        spread_radius=8,
                        blur_radius=16,
                        color=ft.colors.with_opacity(0.25, "black"),
                        offset=(5, 5),
                    ),
                ),
                ft.Divider(height=5, color="transparent"),
                self.loader,
            ],
        )
        self.content = self.column

    # When a search is submitted:
    async def run_compilation(self, e):
        await self.remove_results()
        await asyncio.gather(self.run_loader(), self.get_data())
        await asyncio.sleep(2)  # simulate a loading delay
        await self.stop_loader()
        await self.show_results()

    async def run_loader(self):
        self.loader.value = True
        self.loader.update()

    async def stop_loader(self):
        self.loader.value = 0
        self.loader.update()

    async def show_results(self):
        for container in self.grid.controls:
            container.opacity = 1
            container.update()

    async def remove_results(self):
        for container in self.grid.controls:
            container.opacity = 0
            container.update()

    def redirect_to_url(self, e, route):
        e.page.launch_url(route)

    def custom_text(self, title, subtitle):
        return ft.Text(
            title,
            weight="bold",
            size=14,
            overflow=ft.TextOverflow.ELLIPSIS,
            spans=[ft.TextSpan(text=subtitle, style=ft.TextStyle(weight="w300"))],
            color="white",
        )

    # Load and filter hardcoded article data based on the search query.
    async def get_data(self):
        query = self.inputQuery.value.strip().lower()
        hardcoded_data = [
            {"title": "Saint Luke's", "location": "5th Ave, Taguig, 1634 Metro Manila", "url": "https://www.stlukes.com.ph/"},
            {"title": "PGH", "location": "Taft Ave., Metro Manila", "url": "https://www.pgh.gov.ph/"},
            {"title": "Medical City", "location": "3rd Flr. Waltermart, Chino Roces Ave, Metro Manila", "url": "https://www.themedicalcityclinic.com/waltermart-makati/"},
        ]
        # Filter the articles: if the query is found in the title or location.
        filtered_data = [
            item for item in hardcoded_data
            if query in item["title"].lower() or query in item["location"].lower()
        ]
        temp_list = []
        if filtered_data:
            for index, item in enumerate(filtered_data):
                temp_list.append(
                    ft.Container(
                        on_hover=lambda e, idx=index: self.highlight_box(e, idx),
                        on_click=lambda e, route=item["url"]: self.redirect_to_url(e, route),
                        data=index,
                        border=ft.border.all(1, "#64b687"),
                        border_radius=6,
                        padding=30,
                        shadow=ft.BoxShadow(
                            spread_radius=8,
                            blur_radius=16,
                            color=ft.colors.with_opacity(0.25, "black"),
                            offset=(5, 5),
                        ),
                        animate_opacity=ft.Animation(700, "ease"),
                        content=ft.Column(
                            alignment="spaceBetween",
                            spacing=10,
                            controls=[
                                ft.Text(item["title"], weight="bold", color="white", size=25),
                                ft.Text(item["location"], color="white"),
                            ],
                        ),
                    )
                )
        else:
            # If no articles match the query, show a message.
            temp_list.append(ft.Container(content=ft.Text("No resources found", color="white")))
        self.grid.controls = temp_list
        self.article.content = self.grid
        self.article.update()

    # Hover feature: when hovering over a card, focus on that card while fading others.
    def highlight_box(self, e, hovered_index):
        if e.data == "true":
            for idx, container in enumerate(self.grid.controls):
                container.opacity = 1 if idx == hovered_index else 0.25
                container.update()
        else:
            for container in self.grid.controls:
                container.opacity = 1
                container.update()

# Main App class: arranges the Article component and SearchResult container.
class App(ft.Row):
    def __init__(self, page: ft.Page):
        self.page = page
        self.searchResult = SearchResult(self.page)
        self.article = Article(self.searchResult)
        self.row = ft.ResponsiveRow(alignment="center", vertical_alignment="center")
        super().__init__()

    def build(self):
        self.row.controls.append(self.article)
        self.row.controls.append(ft.VerticalDivider(width=25, color="transparent"))
        self.row.controls.append(self.searchResult)
        return self.row

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#1f262f"
    page.padding = 35
    theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=3, radius=10, main_axis_margin=-20, thumb_color="64b687"
        )
    )
    page.theme = theme
    app = App(page)
    page.add(app.build())
    page.update()
    # No auto-load here: only articles matching the search query will be shown after submitting.
    
if __name__ == "__main__":
    ft.app(main)

