import flet as ft

# ------------------- DetailsAppBar Class -------------------
class DetailsAppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            title=ft.Column(
                controls=[
                    ft.Container(height=3),  
                    ft.Image(
                        src="src/assets/LifeTrackLogo.png",
                        height=55,
                        fit=ft.ImageFit.FIT_HEIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            ),
            center_title=True,
            toolbar_height=40,
            actions=[
                # Wrap PopupMenuButton in a Container to center it vertically
                ft.Container(
                    content=ft.PopupMenuButton(
                        icon=ft.icons.SETTINGS,
                        icon_color="#0cb4cc",  # Set icon color to #0cb4cc
                        items=[
                            ft.PopupMenuItem(
                                text="Profile",
                                on_click=lambda e: print("Profile clicked"),
                            ),
                            ft.PopupMenuItem(
                                text="Logout",
                                on_click=lambda e: page.go("/login"),
                            ),
                        ],
                    ),
                    alignment=ft.alignment.center,  # Center the icon vertically
                ),
            ],
        )

# ------------------- Create Hoverable Container -------------------
def create_container(text1, bgcolor, page, destination=None, hover_color=None):
    container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(text1, size=20, weight="bold"),
                ft.Text("View " + text1, size=16, color=ft.colors.GREY_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border_radius=10,
        bgcolor=bgcolor,
        expand=True,
        alignment=ft.alignment.center,
        scale=ft.transform.Scale(scale=1),  # Initial scale
        animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),  # Smooth animation
    )

    def on_hover(e):
        if e.data == "true":
            # Magnify the container on hover
            container.scale = ft.transform.Scale(scale=1.034)
            container.bgcolor = hover_color if hover_color else bgcolor
        else:
            # Reset the container on hover exit
            container.scale = ft.transform.Scale(scale=1)
            container.bgcolor = bgcolor
        container.update()

    container.on_hover = on_hover

    if destination:
        container.on_click = lambda e: page.go(destination)

    return container

# ------------------- Dashboard -------------------
def show_dashboard(page, username=None):
    print("Dashboard Loaded")

    # Nested row before usage
    def create_nested_row(body_color, page):
        return ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 6},
                    controls=[
                        ft.Container(
                            content=create_container("Vaccination Schedules", ft.colors.AMBER_300, page, destination="/vaccination", hover_color=ft.colors.AMBER_500),
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ],
                ),
                ft.Column(
                    col={"sm": 12, "md": 6},
                    controls=[
                        ft.Container(
                            content=create_container("Health Resources", ft.colors.GREEN_300, page, destination="/health", hover_color=ft.colors.GREEN_500),
                            
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ],
                ),
            ],
            expand=True,
        )

    # Nested column
    def create_nested_column(header_color, body_color, footer_color):
        return ft.Column(
            controls=[
                ft.Container(
                    expand=3,
                    content=ft.Row(
                        controls=[
                            ft.Text(f"Hello, {username if username else 'User'}", size=20, weight="bold"),  # Display the username
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=5,
                    bgcolor=header_color,
                    alignment=ft.alignment.bottom_left,
                ),
                ft.Container(
                    expand=4,
                    content=create_nested_row(ft.colors.WHITE, page),
                    bgcolor=body_color,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=4,
                    content=create_container("Statistics", footer_color, page, destination="/stats", hover_color=ft.colors.RED_100),
        
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
        )

    main_layout = ft.ResponsiveRow(
        controls=[
            ft.Column(
                col={"sm": 12, "md": 9},
                controls=[create_nested_column(ft.colors.BLUE_200, ft.colors.WHITE, ft.colors.RED_200)],
                expand=True,
            ),
            ft.Column(
                col={"sm": 12, "md": 3},
                controls=[
                    ft.Container(
                        content=create_container("Articles", ft.colors.YELLOW_200, page, destination="/news", hover_color=ft.colors.YELLOW_500),
                       
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        ],
        adaptive=True,
        expand=True,
    )

    # Return the dashboard as a view
    return ft.View(
        "/home",
        controls=[main_layout],
        appbar=DetailsAppBar(page),
    )