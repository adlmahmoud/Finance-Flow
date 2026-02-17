import flet as ft
from ui.components.widgets import StatCard, BudgetBar, HeaderBar, TransactionItem

class DashboardPage(ft.Column):
    def __init__(self, controller, user_id):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.spacing = 20
        self.padding = 30
        
        # Initialisation des données
        self._load_data()
        
    def _load_data(self):
        # Récupération des données depuis le contrôleur
        data = self.controller.get_dashboard_data(self.user_id)
        recent_transactions = self.controller.get_transactions(self.user_id, days_back=7)
        
        self.controls = [
            HeaderBar("Tableau de bord", "Aperçu de vos finances"),
            
            # Cartes Statistiques
            ft.Row(
                [
                    StatCard(
                        "Solde Total",
                        f"{data['total_balance']:.2f}€",
                        "account_balance_wallet", # CORRECTION: Nom texte direct
                        "#3b82f6",
                        "+2.5% vs mois dernier"
                    ),
                    StatCard(
                        "Dépenses (Mois)",
                        f"{data['insights']['monthly_expenses']:.2f}€",
                        "credit_card", # CORRECTION: Nom texte direct
                        "#ef4444",
                    ),
                    StatCard(
                        "Économies",
                        f"{data['insights']['savings_rate']:.1f}%",
                        "savings", # CORRECTION: Nom texte direct (ou "attach_money")
                        "#22c55e",
                    ),
                ],
                spacing=20,
            ),
            
            ft.Row(
                [
                    # Section Budgets
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Budgets par Catégorie", size=18, weight="bold"),
                                ft.Column(
                                    [
                                        BudgetBar(
                                            cat,
                                            info["spent"],
                                            info["limit"],
                                            "#3b82f6"
                                        ) for cat, info in data['budget_status'].items()
                                    ],
                                    spacing=15,
                                ),
                            ],
                            spacing=20,
                        ),
                        bgcolor="#0f1419", # ou transparent selon design
                        padding=20,
                        border_radius=10,
                        expand=2,
                    ),
                    
                    # Section Transactions Récentes
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("Récemment", size=18, weight="bold"),
                                        ft.TextButton("Voir tout"),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Column(
                                    [TransactionItem(t) for t in recent_transactions[:5]],
                                    spacing=0,
                                ),
                            ],
                            spacing=20,
                        ),
                        bgcolor="#0f1419",
                        padding=20,
                        border_radius=10,
                        expand=1,
                    ),
                ],
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ]