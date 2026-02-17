import flet as ft
from ui.components.widgets import HeaderBar, TransactionItem

class TransactionsPage(ft.Column):
    def __init__(self, controller, user_id):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.padding = 30
        
        self.controls = [
            HeaderBar("Transactions", "Historique complet"),
            self._build_filters(),
            ft.Container(height=20),
            self._build_transactions_list(),
        ]
        
    def _build_filters(self):
        return ft.Row(
            [
                ft.TextField(
                    hint_text="Rechercher...",
                    prefix_icon=ft.icons.SEARCH,
                    border_radius=10,
                    bgcolor="#1e293b",
                    border_color="transparent",
                    height=45,
                    content_padding=10,
                    expand=True,
                ),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Tous"),
                        ft.dropdown.Option("Dépenses"),
                        ft.dropdown.Option("Revenus"),
                    ],
                    value="Tous",
                    width=150,
                    bgcolor="#1e293b",
                    border_radius=10,
                    border_color="transparent",
                    height=45,
                ),
                ft.IconButton(
                    icon=ft.icons.FILTER_LIST,
                    bgcolor="#1e293b",
                    icon_color="white",
                ),
                ft.ElevatedButton(
                    "Synchroniser",
                    icon=ft.icons.SYNC,
                    bgcolor="#3b82f6",
                    color="white",
                    height=45,
                    on_click=self._sync_transactions,
                ),
            ],
            spacing=15,
        )

    def _build_transactions_list(self):
        transactions = self.controller.get_transactions(self.user_id, days_back=90)
        
        if not transactions:
            return ft.Container(
                content=ft.Text("Aucune transaction trouvée", color="#94a3b8"),
                alignment=ft.alignment.center,
                padding=50,
            )

        return ft.Column(
            [TransactionItem(t) for t in transactions],
            spacing=0,
        )

    def _sync_transactions(self, e):
        # Simulation de sync
        self.controller.sync_transactions_from_bank(self.user_id)
        # Recharger la page (ou juste la liste)
        # Pour faire simple ici on peut recharger la vue
        self.controls[-1] = self._build_transactions_list()
        self.update()