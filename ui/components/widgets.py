import flet as ft

class StatCard(ft.Container):
    def __init__(self, title: str, value: str, icon_name: str, color: str, trend: str = None):
        super().__init__()
        self.title = title
        self.value = value
        self.icon_name = icon_name
        self.color = color
        self.trend = trend
        
        # Configuration du Container
        self.padding = 20
        self.bgcolor = "#1e293b"
        self.border_radius = 10
        self.expand = True
        
        # Contenu
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(self.icon_name, color="white"),
                            padding=10,
                            bgcolor=self.color,
                            border_radius=10,
                        ),
                        ft.Column(
                            [
                                ft.Text(self.title, size=12, color="#94a3b8"),
                                ft.Text(self.value, size=20, weight="bold"),
                            ],
                            spacing=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ]
        )
        
        if self.trend:
            trend_color = "#22c55e" if self.trend.startswith("+") else "#ef4444"
            self.content.controls.append(
                ft.Container(
                    content=ft.Text(self.trend, size=12, color=trend_color),
                    margin=ft.margin.only(top=10),
                )
            )

class BudgetBar(ft.Container):
    def __init__(self, category: str, spent: float, limit: float, color: str):
        super().__init__()
        self.category = category
        self.spent = spent
        self.limit = limit
        self.color = color
        
        percentage = min(self.spent / self.limit, 1.0) if self.limit > 0 else 0
        
        self.bgcolor = "#1e293b"
        self.padding = 15
        self.border_radius = 10
        
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(self.category, weight="bold"),
                        ft.Text(f"{int(percentage * 100)}%", color="#94a3b8"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ProgressBar(
                    value=percentage,
                    color=self.color,
                    bgcolor="#334155",
                    height=8,
                ),
                ft.Row(
                    [
                        ft.Text(f"{self.spent:.2f}€", size=12, color="#94a3b8"),
                        ft.Text(f"{self.limit:.2f}€", size=12, color="#94a3b8"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10,
        )

class HeaderBar(ft.Container):
    def __init__(self, title: str, subtitle: str = None):
        super().__init__()
        self.padding = ft.padding.symmetric(vertical=20)
        
        title_col = ft.Column(
            [
                ft.Text(title, size=28, weight="bold"),
            ],
            spacing=5,
        )
        
        if subtitle:
            title_col.controls.append(ft.Text(subtitle, color="#94a3b8"))
            
        self.content = ft.Row(
            [
                title_col,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NOTIFICATIONS,
                            icon_color="#94a3b8",
                        ),
                        ft.CircleAvatar(
                            content=ft.Text("JD"),
                            bgcolor="#3b82f6",
                            radius=18,
                        ),
                    ],
                    spacing=10,
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

class TransactionItem(ft.Container):
    def __init__(self, transaction):
        super().__init__()
        self.transaction = transaction
        
        is_income = self.transaction.transaction_type == "Revenu"
        amount_color = "#22c55e" if is_income else "#ef4444"
        amount_sign = "+" if is_income else "-"
        
        self.padding = ft.padding.symmetric(vertical=10, horizontal=15)
        self.bgcolor = "#1e293b"
        self.border_radius = 8
        self.margin = ft.margin.only(bottom=8)
        
        self.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.SHOPPING_BAG if not is_income else ft.icons.ATTACH_MONEY,
                                color="white",
                                size=16
                            ),
                            padding=8,
                            bgcolor="#334155",
                            border_radius=8,
                        ),
                        ft.Column(
                            [
                                ft.Text(self.transaction.description, weight="bold"),
                                ft.Text(
                                    self.transaction.date.strftime("%d %b %Y"),
                                    size=12,
                                    color="#94a3b8"
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Text(
                    f"{amount_sign}{abs(self.transaction.amount):.2f}€",
                    weight="bold",
                    color=amount_color,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )