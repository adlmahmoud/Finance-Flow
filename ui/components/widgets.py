"""Reusable UI components for Flet application."""

import flet as ft
from typing import Callable, Optional, Any


class StatCard(ft.UserControl):
    """Stat card component for displaying key metrics."""

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        icon: str = "📊",
        color: str = "#1f77b4",
    ):
        """
        Initialize stat card.
        
        Args:
            title: Card title
            value: Main value to display
            subtitle: Optional subtitle
            icon: Icon emoji
            color: Accent color
        """
        super().__init__()
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
        self.color = color

    def build(self):
        """Build stat card."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        value=self.icon,
                        size=32,
                        color=self.color,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                self.title,
                                size=14,
                                color="#999",
                            ),
                            ft.Text(
                                self.value,
                                size=24,
                                weight="bold",
                            ),
                            ft.Text(
                                self.subtitle,
                                size=12,
                                color="#999",
                            ) if self.subtitle else ft.Text(""),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                ],
                spacing=16,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=16,
            bgcolor="#1e1e1e",
            border_radius=8,
            border=ft.border.all(1, "#333"),
        )


class TransactionItem(ft.UserControl):
    """Transaction list item component."""

    def __init__(
        self,
        category: str,
        description: str,
        amount: str,
        date: str,
        is_income: bool = False,
        on_click: Optional[Callable] = None,
    ):
        """
        Initialize transaction item.
        
        Args:
            category: Transaction category
            description: Transaction description
            amount: Transaction amount
            date: Transaction date
            is_income: Whether it's income (green) or expense (red)
            on_click: Click handler
        """
        super().__init__()
        self.category = category
        self.description = description
        self.amount = amount
        self.date = date
        self.is_income = is_income
        self.on_click_handler = on_click

    def build(self):
        """Build transaction item."""
        amount_color = "#10b981" if self.is_income else "#ef4444"
        amount_prefix = "+" if self.is_income else "-"
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        name="🏷️" if not self.is_income else "💰",
                        color=amount_color,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                self.description,
                                weight="bold",
                                size=14,
                            ),
                            ft.Text(
                                self.category,
                                size=12,
                                color="#999",
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"{amount_prefix}{self.amount}€",
                                weight="bold",
                                size=14,
                                color=amount_color,
                            ),
                            ft.Text(
                                self.date,
                                size=12,
                                color="#999",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=12,
            bgcolor="#1e1e1e",
            border_radius=8,
            border=ft.border.all(1, "#333"),
            on_click=self.on_click_handler,
        )


class BudgetBar(ft.UserControl):
    """Budget progress bar component."""

    def __init__(
        self,
        category: str,
        spent: float,
        limit: float,
    ):
        """
        Initialize budget bar.
        
        Args:
            category: Category name
            spent: Amount spent
            limit: Budget limit
        """
        super().__init__()
        self.category = category
        self.spent = spent
        self.limit = limit

    def build(self):
        """Build budget bar."""
        percentage = min(100, (self.spent / self.limit * 100)) if self.limit > 0 else 0
        is_exceeded = self.spent > self.limit
        bar_color = "#ef4444" if is_exceeded else "#3b82f6"

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                self.category,
                                weight="bold",
                                size=12,
                            ),
                            ft.Text(
                                f"{self.spent:.2f}€ / {self.limit:.2f}€",
                                size=12,
                                color="#999",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.ProgressBar(
                        value=percentage / 100,
                        color=bar_color,
                        height=8,
                        border_radius=4,
                    ),
                    ft.Text(
                        f"{percentage:.0f}%" if not is_exceeded else "Dépassé!",
                        size=11,
                        color="#999" if not is_exceeded else "#ef4444",
                    ),
                ],
                spacing=4,
            ),
            padding=12,
            bgcolor="#1e1e1e",
            border_radius=8,
            border=ft.border.all(1, "#333"),
        )


class HeaderBar(ft.UserControl):
    """App header bar component."""

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        on_menu_click: Optional[Callable] = None,
    ):
        """
        Initialize header bar.
        
        Args:
            title: Header title
            subtitle: Optional subtitle
            on_menu_click: Menu button click handler
        """
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.on_menu_click_handler = on_menu_click

    def build(self):
        """Build header bar."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        name="menu",
                        size=24,
                        color="#fff",
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                self.title,
                                size=20,
                                weight="bold",
                            ),
                            ft.Text(
                                self.subtitle,
                                size=12,
                                color="#999",
                            ) if self.subtitle else ft.Text(""),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Icon(
                        name="notifications",
                        size=20,
                        color="#fff",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
            bgcolor="#0a0e27",
            border_radius=0,
        )
