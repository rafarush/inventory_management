import uuid
from django.db import models
from inventory_management.modules.product.models import Product  # ajusta la ruta según tu proyecto


class ChargeCart(models.Model):
    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("finalizado", "Finalizado"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="charges"
    )
    amount_sent = models.PositiveIntegerField(default=0, null=True, blank=True)
    price_sent = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    amount_received = models.PositiveIntegerField(null=True, blank=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    revenue_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    money_returned = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendiente"
    )


    def __str__(self):
        return f"{self.product.id}"
