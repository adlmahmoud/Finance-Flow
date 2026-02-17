"""
Transactions Page - View and manage all transactions.
"""

import flet as ft
from datetime import datetime, timedelta
from typing import Optional

from controllers.app_controller import AppController
from ui.components.widgets import TransactionItem, HeaderBar


class TransactionsPage(ft.UserControl):
    """Transactions management page."""

    def __init__(self, controller: AppController, user_id: int):
        """
        Initialize transactions page.
        
        Args:
            controller: Application controller
            user_id: Current user ID
        """
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.filter_days = 30
        self.transactions_list = ft.Column(spacing=8, auto_scroll=True)

    def build(self):
        """Build transactions page."""
        self._load_transactions()

        return ft.Column(
            [
                HeaderBar(
                    title="Transactions",
                    subtitle="Historique de tous vos mouvements",
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            self._build_filters(),
                            self.transactions_list,
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _build_filters(self) -> ft.Container:
        """Build filter controls."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Dropdown(
                        label="Période",
                        value="30",
                        options=[
                            ft.dropdown.Option("7"),
                            ft.dropdown.Option("30"),
                            ft.dropdown.Option("90"),
                            ft.dropdown.Option("365"),
                        ],
                        on_change=self._on_filter_change,
                        width=200,
                    ),
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        tooltip="Synchroniser depuis la banque",
                        on_click=self._on_sync_click,
                    ),
                ],
                spacing=12,
            ),
            padding=0,
        )

    def _load_transactions(self):
        """Load and display transactions."""
        try:
            transactions = self.controller.get_transactions(
                self.user_id,
                days_back=self.filter_days,
            )

            self.transactions_list.controls.clear()

            if not transactions:
                self.transactions_list.controls.append(
                    ft.Text(
                        "Aucune transaction trouvée",
                        color="#999",
                        size=14,
                    )
                )
            else:
                for txn in transactions:
                    self.transactions_list.controls.append(
                        TransactionItem(
                            category=txn.category.value,
                            description=txn.description,
                            amount=f"{txn.amount:.2f}",
                            date=txn.date.strftime("%d/%m/%Y"),
                            is_income=(txn.transaction_type.value == "Revenu"),
                        )
                    )

            self.update()
        except Exception as e:
            self.transactions_list.controls.clear()
            self.transactions_list.controls.append(
                ft.Text(
                    f"Erreur: {str(e)}",
                    color="#ef4444",
                    size=14,
                )
            )
            self.update()

    def _on_filter_change(self, e):
        """Handle filter change."""
        self.filter_days = int(e.control.value)
        self._load_transactions()

    def _on_sync_click(self, e):
        """Handle sync button click."""
        try:
            # Show loading state
            e.control.disabled = True
            e.control.update()

            # Sync transactions
            results = self.controller.sync_transactions_from_bank(self.user_id)

            # Reload transactions
            self._load_transactions()

            # Show success
            e.control.disabled = False
            e.control.update()
        except Exception as ex:
            e.control.disabled = False
            e.control.update()
