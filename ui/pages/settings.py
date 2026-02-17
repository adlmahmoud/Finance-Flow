import flet as ft
from ui.components.widgets import HeaderBar

class SettingsPage(ft.Column):
    def __init__(self, controller, user_id, on_logout):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.on_logout = on_logout
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.padding = 30
        
        self.controls = [
            HeaderBar("Paramètres", "Préférences de l'application"),
            
            ft.Container(height=20),
            
            self._build_section(
                "Compte",
                [
                    self._build_setting_item("Email", "john@example.com", "email"),
                    self._build_setting_item("Mot de passe", "********", "lock"),
                ]
            ),
            
            ft.Container(height=20),
            
            self._build_section(
                "Préférences",
                [
                    self._build_setting_item("Devise", "EUR (€)", "money"),
                    self._build_setting_item("Thème", "Sombre", "dark_mode"),
                    self._build_setting_item("Notifications", "Activées", "notifications"),
                ]
            ),
            
            ft.Container(height=40),
            
            ft.ElevatedButton(
                "Se déconnecter",
                icon="logout",
                bgcolor="#ef4444",
                color="white",
                height=50,
                width=200,
                on_click=lambda e: self.on_logout(),
            ),
        ]

    def _build_section(self, title, items):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=18, weight="bold", color="#3b82f6"),
                    ft.Column(items, spacing=0),
                ],
                spacing=15,
            ),
            bgcolor="#1e293b",
            padding=20,
            border_radius=10,
        )

    def _build_setting_item(self, title, value, icon):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, size=20, color="#94a3b8"),
                            ft.Text(title, size=16),
                        ],
                        spacing=15,
                    ),
                    ft.Row(
                        [
                            ft.Text(value, color="#94a3b8"),
                            ft.Icon("chevron_right", color="#64748b"),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(vertical=15),
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#334155")),
        )