# inventory_management/modules/status_cart/apps.py
from django.apps import AppConfig


class StatusCartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory_management.modules.cart_status"

    def ready(self):
        import inventory_management.modules.cart_status.signals
