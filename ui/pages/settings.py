"""
Settings Page - User settings and configuration.
"""

import flet as ft
from typing import Callable, Optional

from controllers.app_controller import AppController
from ui.components.widgets import HeaderBar
from models.database import TransactionCategory


class SettingsPage(ft.UserControl):
    """Settings and configuration page."""

    def __init__(
        self,
        controller: AppController,
        user_id: int,
        on_logout: Optional[Callable] = None,
    ):
        """
        Initialize settings page.
        
        Args:
            controller: Application controller
            user_id: Current user ID
            on_logout: Logout callback
        """
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.on_logout_handler = on_logout

    def build(self):
        """Build settings page."""
        return ft.Column(
            [
                HeaderBar(
                    title="Paramètres",
                    subtitle="Gérez vos préférences",
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            self._build_account_section(),
                            ft.Divider(height=1),
                            self._build_budget_section(),
                            ft.Divider(height=1),
                            self._build_bank_api_section(),
                            ft.Divider(height=1),
                            self._build_app_section(),
                        ],
                        spacing=8,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _build_account_section(self) -> ft.Container:
        """Build account settings section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Compte",
                        size=16,
                        weight="bold",
                    ),
                    ft.Row(
                        [
                            ft.Icon(name=ft.icons.PERSON),
                            ft.Column(
                                [
                                    ft.Text("Email", size=12, color="#999"),
                                    ft.Text("user@example.com", weight="bold"),
                                ],
                                expand=True,
                            ),
                            ft.Icon(name=ft.icons.EDIT),
                        ],
                    ),
                    ft.Divider(height=1, color="#333"),
                    ft.Row(
                        [
                            ft.Icon(name=ft.icons.LOCK),
                            ft.Column(
                                [
                                    ft.Text("Mot de passe", size=12, color="#999"),
                                    ft.Text("●●●●●●●●", weight="bold"),
                                ],
                                expand=True,
                            ),
                            ft.Icon(name=ft.icons.EDIT),
                        ],
                    ),
                ],
                spacing=12,
            ),
            padding=12,
        )

    def _build_budget_section(self) -> ft.Container:
        """Build budget settings section."""
        budget_inputs = []

        for category in TransactionCategory:
            budget_inputs.append(
                ft.Row(
                    [
                        ft.Text(category.value, expand=True),
                        ft.TextField(
                            label="Limite (€)",
                            value="500",
                            width=120,
                            input_filter=ft.NumbersOnlyInputFilter(),
                        ),
                    ],
                    spacing=8,
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Budgets par Catégorie",
                        size=16,
                        weight="bold",
                    ),
                    ft.Column(
                        budget_inputs,
                        spacing=8,
                    ),
                    ft.ElevatedButton(
                        text="Enregistrer les budgets",
                        on_click=self._on_save_budgets,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            padding=12,
        )

    def _build_bank_api_section(self) -> ft.Container:
        """Build bank API configuration section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Intégration Bancaire",
                        size=16,
                        weight="bold",
                    ),
                    ft.Text(
                        "Connectez votre compte bancaire pour synchroniser automatiquement vos transactions",
                        size=12,
                        color="#999",
                    ),
                    ft.Dropdown(
                        label="Fournisseur",
                        value="mock",
                        options=[
                            ft.dropdown.Option("mock", "Demo (Test)"),
                            ft.dropdown.Option("plaid", "Plaid"),
                            ft.dropdown.Option("gocardless", "GoCardless"),
                        ],
                    ),
                    ft.TextField(
                        label="Clé API (optionnel)",
                        password=True,
                        hint_text="Votre clé API",
                    ),
                    ft.ElevatedButton(
                        text="Connecter un compte bancaire",
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            padding=12,
        )

    def _build_app_section(self) -> ft.Container:
        """Build app settings section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Application",
                        size=16,
                        weight="bold",
                    ),
                    ft.Row(
                        [
                            ft.Text("Thème sombre", expand=True),
                            ft.Switch(value=True),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Text("Notifications", expand=True),
                            ft.Switch(value=True),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=1, color="#333"),
                    ft.TextButton(
                        text="❌ Déconnexion",
                        on_click=self._on_logout_click,
                    ),
                ],
                spacing=12,
            ),
            padding=12,
        )

    def _on_save_budgets(self, e):
        """Save budget settings."""
        # TODO: Implement budget saving
        pass

    def _on_logout_click(self, e):
        """Handle logout."""
        if self.on_logout_handler:
            self.on_logout_handler()
