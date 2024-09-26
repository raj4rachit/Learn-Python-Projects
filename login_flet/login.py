import flet as ft
import re
import requests
from datetime import datetime
import threading

def main(page: ft.Page):
    user_info = {"is_logged_in": False, "name": "", "profile_image": "", "data": "", "token": ""}

    def update_header():
        #header.content.clean()
        if user_info["is_logged_in"]:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header.content.add([
                ft.Image(src="https://hrms.schedulesoftware.net/storage/uploads/profiles/1699341152.jpg", width=100, height=50),
                ft.Row(controls=[
                    ft.Container(
                        content=ft.Image(src=user_info["profile_image"], width=50, height=50),
                        width=50,
                        height=50,
                        border_radius=25,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    ft.Text(value=user_info["name"]),
                    ft.Text(value=current_time),
                    ft.ElevatedButton(text="Logout", on_click=logout),
                ], alignment=ft.MainAxisAlignment.END)
            ])
        else:
            pass
            #header.content.add(ft.Image(src="https://technobrains.io/wp-content/uploads/2021/06/logo.svg", width=100, height=50))
        page.update()

    def update_footer():
        if user_info["is_logged_in"]:
            footer.content.clean()  # Clear the content of the footer container
            footer.content.add(
                ft.Row(
                    controls=[
                        ft.TextButton(text="Dashboard", on_click=lambda e: fetch_data("dashboard")),
                        ft.TextButton(text="Leave", on_click=lambda e: fetch_data("leave")),
                        ft.TextButton(text="Timesheet", on_click=lambda e: fetch_data("timesheet")),
                        ft.TextButton(text="Calendar", on_click=lambda e: fetch_data("calendar")),
                        ft.TextButton(text="Holiday", on_click=lambda e: fetch_data("holiday")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            )
        else:
            footer.content.clean()
            footer.content.add(
                ft.Row(
                    controls=[
                        ft.Text(value="© 2024 Technobrains", size=12, alignment=ft.alignment.center)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            )
        page.update()

    def login(e):
        page.splash = ft.ProgressBar()
        page.update()
        email_value = email.value
        password_value = password.value

        # Email validation
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email_value):
            result.value = "Invalid email address"
            result.color = ft.colors.RED
            page.splash = None
            login_button.disabled = False
            page.update()
            return

        # Password validation
        if len(password_value) < 6:
            result.value = "Password must be at least 6 characters long"
            result.color = ft.colors.RED
            page.splash = None
            login_button.disabled = False
            page.update()
            return

        # API call to check credentials
        response = requests.post("https://hrms.schedulesoftware.net/api/login",
                                 json={"email": email_value, "password": password_value})
        if response.status_code == 200 and response.json().get("status"):
            user_info["is_logged_in"] = True
            user_info["data"] = response.json().get("data")
            user_info["name"] = user_info["data"]["user"]["full_name"]
            user_info["profile_image"] = user_info["data"]["user"]["profile_picture_url"]
            user_info["token"] = user_info["data"]["token"]
            result.value = "Login successful!"
            result.color = ft.colors.GREEN
            page.splash = None
            login_button.disabled = False
            page.update()
            update_header()
            update_footer()
            start_refresh_token_thread()
            show_dashboard()
        else:
            result.value = response.json().get("error")
            result.color = ft.colors.RED
            page.splash = None
            login_button.disabled = False
            page.update()

    def logout(e):
        user_info["is_logged_in"] = False
        user_info["name"] = ""
        user_info["profile_image"] = ""
        update_header()
        update_footer()
        show_login()

    def show_dashboard():
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    header,
                    ft.Text(value="Welcome to the Dashboard", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(value="Here is your data:"),
                    ft.Text(value=str(user_info["data"])),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )
        page.add(footer)
        page.update()

    def show_login():
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    header,
                    ft.Text(value="Login", weight=ft.FontWeight.BOLD, style="displayLarge"),
                    email,
                    password,
                    login_button,
                    result,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )
        page.add(footer)
        page.update()

    def fetch_data(tab):
        endpoint_map = {
            "dashboard": "dashboard",
            "leave": "leave",
            "timesheet": "timesheet",
            "calendar": "calendar",
            "holiday": "holiday"
        }
        endpoint = endpoint_map.get(tab, "dashboard")
        response = requests.get(f"https://hrms.schedulesoftware.net/api/{endpoint}",
                                headers={"Authorization": f"Bearer {user_info['token']}"})
        if response.status_code == 200 and response.json().get("status"):
            user_info["data"] = response.json().get("data")
            show_tab_content(tab)
        else:
            result.value = response.json().get("error")
            result.color = ft.colors.RED
            page.update()

    def show_tab_content(tab):
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    header,
                    ft.Text(value=f"Welcome to the {tab.capitalize()} Page", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(value="Here is your data:"),
                    ft.Text(value=str(user_info["data"])),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )
        page.add(footer)
        page.update()

    def refresh_token():
        while user_info["is_logged_in"]:
            response = requests.post("https://hrms.schedulesoftware.net/api/refresh-token",
                                     headers={"Authorization": f"Bearer {user_info['token']}"})
            if response.status_code == 200 and response.json().get("status"):
                user_info["token"] = response.json().get("data")["token"]
                user_info["data"] = response.json().get("data")
                update_dashboard()
            threading.Event().wait(300)  # Wait for 5 minutes (300 seconds) before refreshing again

    def update_dashboard():
        if user_info["is_logged_in"]:
            show_dashboard()

    def start_refresh_token_thread():
        refresh_thread = threading.Thread(target=refresh_token)
        refresh_thread.start()

    # Create input fields for email and password
    email = ft.TextField(label="Email", width=300)
    password = ft.TextField(label="Password", password=True, width=300)

    # Create a button to trigger the login function
    login_button = ft.FilledButton(text="Login", on_click=login, width=200, height=50)

    # Create a text field to display the result
    result = ft.Text(value="", size=20)

    # Create header and footer
    header = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    header = ft.Container(
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        height=100,
        expand=False
    )
    footer = ft.Container(
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        padding=10,
        bgcolor=ft.colors.GREY_300,
        height=50,
        expand=False
    )

    page.title = "HRMS"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "spaceBetween"
    page.window_resizable = False
    page.window_width = 1000
    page.window_height = 700

    # Update header and footer initially
    update_header()
    update_footer()

    # Show login initially
    show_login()

# Run the app
ft.app(target=main)
