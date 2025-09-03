# inventory_management/modules/status_cart/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CartStatus


@receiver(post_migrate)
def ensure_cart_statuses(sender, **kwargs):
    required_statuses = ["PENDIENTE", "FINALIZADO"]

    for status in required_statuses:
        CartStatus.objects.get_or_create(status=status)
