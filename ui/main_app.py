"""
Main Application - FinanceFlow
Modern expense management with bank API integration.
"""

import flet as ft
from typing import Optional
from loguru import logger

from config.settings import settings
from controllers.app_controller import AppController
from models.database import User
from ui.pages.dashboard import DashboardPage
from ui.pages.transactions import TransactionsPage
from ui.pages.settings import SettingsPage


class FinanceFlowApp:
    """Main application class."""

    def __init__(self, page: ft.Page):
        """
        Initialize the application.
        
        Args:
            page: Flet page object
        """
        self.page = page
        self.controller = AppController()
        self.current_user: Optional[User] = None
        
        # Configure page
        self.page.title = f"{settings.APP_NAME} v{settings.APP_VERSION}"
        self.page.window.height = settings.WINDOW_HEIGHT
        self.page.window.width = settings.WINDOW_WIDTH
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        
        # Navigation variables
        self.current_page = "login"
        self.main_content = ft.Container()
        
        logger.info(f"Initializing {settings.APP_NAME}")

    def build(self):
        """Build the application UI."""
        self.page.clean()
        self.page.add(self._build_main_layout())

    def _build_main_layout(self) -> ft.Container:
        """Build the main application layout."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self._build_sidebar(),
                            ft.VerticalDivider(width=1),
                            self.main_content,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
            bgcolor="#0a0e27",
        )

    def _build_sidebar(self) -> ft.Container:
        """Build navigation sidebar."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(name=ft.icons.SAVINGS, size=32, color="#3b82f6"),
                                ft.Text(
                                    "FinanceFlow",
                                    size=18,
                                    weight="bold",
                                ),
                                ft.Text(
                                    "v2.0",
                                    size=10,
                                    color="#999",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=20,
                        border_radius=8,
                    ),
                    ft.Divider(height=1, color="#333"),
                    ft.Column(
                        [
                            self._nav_button("📊 Dashboard", "dashboard"),
                            self._nav_button("💳 Transactions", "transactions"),
                            self._nav_button("📈 Analyse", "analytics"),
                            self._nav_button("⚙️ Paramètres", "settings"),
                        ],
                        spacing=0,
                    ),
                    ft.Column(expand=True),
                    ft.Divider(height=1, color="#333"),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.PERSON, size=24),
                                ft.Column(
                                    [
                                        ft.Text("John Doe", weight="bold", size=12),
                                        ft.Text("john@example.com", size=10, color="#999"),
                                    ],
                                    expand=True,
                                    spacing=2,
                                ),
                            ],
                            spacing=12,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=16,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            width=250,
            bgcolor="#0f1419",
            border_radius=0,
        )

    def _nav_button(self, text: str, page_name: str) -> ft.Container:
        """Create a navigation button."""
        return ft.Container(
            content=ft.Text(
                text,
                size=14,
                color="#ccc",
            ),
            padding=ft.padding.symmetric(vertical=12, horizontal=16),
            on_hover=lambda e: self._on_nav_hover(e, True),
            on_click=lambda e: self._navigate(page_name),
        )

    def _on_nav_hover(self, e, is_hover: bool):
        """Handle navigation button hover."""
        if is_hover:
            e.control.bgcolor = "#1e293b"
        else:
            e.control.bgcolor = None
        e.control.update()

    def _navigate(self, page_name: str):
        """Navigate to a different page."""
        self.current_page = page_name
        self._update_main_content()

    def _update_main_content(self):
        """Update the main content area based on current page."""
        self.main_content.content = self._get_page_content()
        self.main_content.update()

    def _get_page_content(self) -> ft.Control:
        """Get the content for the current page."""
        if not self.current_user:
            return self._build_login_page()

        if self.current_page == "dashboard":
            return DashboardPage(self.controller, self.current_user.id)
        elif self.current_page == "transactions":
            return TransactionsPage(self.controller, self.current_user.id)
        elif self.current_page == "analytics":
            return self._build_analytics_page()
        elif self.current_page == "settings":
            return SettingsPage(
                self.controller,
                self.current_user.id,
                on_logout=self._logout,
            )
        else:
            return DashboardPage(self.controller, self.current_user.id)

    def _build_login_page(self) -> ft.Container:
        """Build login page."""
        username_field = ft.TextField(
            label="Nom d'utilisateur",
            width=300,
        )
        password_field = ft.TextField(
            label="Mot de passe",
            password=True,
            width=300,
        )
        error_text = ft.Text("", color="#ef4444", size=12)

        def on_login_click(e):
            """Handle login button click."""
            username = username_field.value
            password = password_field.value

            if not username or not password:
                error_text.value = "Veuillez remplir tous les champs"
                error_text.update()
                return

            # Try to authenticate
            user = self.controller.authenticate_user(username, password)

            if user:
                self.current_user = user
                self.current_page = "dashboard"
                self.build()
            else:
                error_text.value = "Nom d'utilisateur ou mot de passe incorrect"
                error_text.update()

        def on_signup_click(e):
            """Handle signup button click."""
            username = username_field.value
            password = password_field.value

            if not username or not password:
                error_text.value = "Veuillez remplir tous les champs"
                error_text.update()
                return

            try:
                user = self.controller.create_user(
                    username=username,
                    email=f"{username}@example.com",
                    password=password,
                    full_name=username,
                )
                self.current_user = user
                self.current_page = "dashboard"
                self.build()
            except Exception as ex:
                error_text.value = str(ex)
                error_text.update()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Column(
                        [
                            ft.Icon(
                                name=ft.icons.SAVINGS,
                                size=64,
                                color="#3b82f6",
                            ),
                            ft.Text(
                                settings.APP_NAME,
                                size=32,
                                weight="bold",
                            ),
                            ft.Text(
                                "Gestion de dépenses moderne",
                                size=14,
                                color="#999",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    ft.Container(height=30),
                    ft.Column(
                        [
                            username_field,
                            password_field,
                            error_text,
                            ft.ElevatedButton(
                                text="Se connecter",
                                on_click=on_login_click,
                                width=300,
                            ),
                            ft.Row(
                                [
                                    ft.Text("Pas de compte?", size=12, color="#999"),
                                    ft.TextButton(
                                        text="S'inscrire",
                                        on_click=on_signup_click,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )

    def _build_analytics_page(self) -> ft.Container:
        """Build analytics page."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "📊 Analyse Financière",
                        size=24,
                        weight="bold",
                    ),
                    ft.Text(
                        "Fonctionnalité en développement",
                        color="#999",
                        size=14,
                    ),
                ],
                padding=16,
                spacing=12,
            ),
        )

    def _logout(self):
        """Logout the current user."""
        self.current_user = None
        self.current_page = "login"
        self.build()


def main(page: ft.Page):
    """Main entry point for Flet application."""
    app = FinanceFlowApp(page)
    app.build()


if __name__ == "__main__":
    ft.app(main)
