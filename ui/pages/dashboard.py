"""
Dashboard Page - Main view showing financial overview.
"""

import flet as ft
from datetime import datetime
from typing import Callable, Optional

from controllers.app_controller import AppController
from ui.components.widgets import StatCard, BudgetBar, HeaderBar, TransactionItem


class DashboardPage(ft.UserControl):
    """Dashboard page component."""

    def __init__(self, controller: AppController, user_id: int):
        """
        Initialize dashboard page.
        
        Args:
            controller: Application controller
            user_id: Current user ID
        """
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.page_expanded = True

    def build(self):
        """Build dashboard page."""
        return ft.Column(
            [
                HeaderBar(
                    title="FinanceFlow Dashboard",
                    subtitle=f"Bienvenue! Aujourd'hui {datetime.now().strftime('%d/%m/%Y')}",
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            self._build_stats_row(),
                            self._build_charts_section(),
                            self._build_budgets_section(),
                            self._build_transactions_section(),
                        ],
                        spacing=16,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _build_stats_row(self) -> ft.Row:
        """Build key statistics row."""
        # Get dashboard data
        try:
            data = self.controller.get_dashboard_data(self.user_id)
            total_balance = data.get("total_balance", 0)
            insights = data.get("insights", {})
            avg_expense = insights.get("average_monthly_expense", 0)
        except Exception as e:
            total_balance = 0
            avg_expense = 0

        return ft.Row(
            [
                StatCard(
                    title="Solde Total",
                    value=f"{total_balance:.2f}€",
                    subtitle="Tous les comptes",
                    icon="💳",
                    color="#10b981",
                ),
                StatCard(
                    title="Dépenses Mensuelles",
                    value=f"{avg_expense:.2f}€",
                    subtitle="Moyenne",
                    icon="💸",
                    color="#ef4444",
                ),
                StatCard(
                    title="Budget Restant",
                    value=f"{max(0, 3000 - avg_expense):.2f}€",
                    subtitle="Ce mois",
                    icon="🎯",
                    color="#3b82f6",
                ),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_charts_section(self) -> ft.Container:
        """Build charts section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Tendances",
                        size=18,
                        weight="bold",
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "📈 Graphique des dépenses par catégorie",
                                    size=14,
                                    color="#999",
                                ),
                                ft.Text(
                                    "Les données de ce mois seront affichées ici",
                                    size=12,
                                    color="#666",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        height=250,
                        bgcolor="#1e1e1e",
                        border_radius=8,
                        border=ft.border.all(1, "#333"),
                    ),
                ],
                spacing=12,
            ),
            padding=0,
        )

    def _build_budgets_section(self) -> ft.Container:
        """Build budgets section."""
        try:
            data = self.controller.get_dashboard_data(self.user_id)
            budgets = data.get("budget_status", [])
        except Exception:
            budgets = []

        budget_items = []
        for budget in budgets:
            budget_items.append(
                BudgetBar(
                    category=budget["category"],
                    spent=budget["spent"],
                    limit=budget["limit"],
                )
            )

        if not budget_items:
            budget_items.append(
                ft.Text(
                    "Aucun budget configuré",
                    color="#999",
                    size=14,
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Budgets",
                        size=18,
                        weight="bold",
                    ),
                    ft.Column(
                        budget_items,
                        spacing=8,
                    ),
                ],
                spacing=12,
            ),
            padding=0,
        )

    def _build_transactions_section(self) -> ft.Container:
        """Build recent transactions section."""
        try:
            transactions = self.controller.get_transactions(self.user_id, days_back=7)
        except Exception:
            transactions = []

        transaction_items = []
        for txn in transactions[:10]:  # Show last 10
            transaction_items.append(
                TransactionItem(
                    category=txn.category.value,
                    description=txn.description,
                    amount=f"{txn.amount:.2f}",
                    date=txn.date.strftime("%d/%m/%Y"),
                    is_income=(txn.transaction_type.value == "Revenu"),
                )
            )

        if not transaction_items:
            transaction_items.append(
                ft.Text(
                    "Aucune transaction récente",
                    color="#999",
                    size=14,
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Transactions Récentes",
                                size=18,
                                weight="bold",
                            ),
                            ft.TextButton(
                                text="Voir tout",
                                on_click=None,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Column(
                        transaction_items,
                        spacing=8,
                        height=400,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                spacing=12,
            ),
            padding=0,
        )

    def refresh(self):
        """Refresh dashboard data."""
        self.update()
