import uuid
from django.db import models
from inventory_management.modules.product.models import Product  # ajusta la ruta según tu proyecto


class ChargeCart(models.Model):
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
    amount_sent = models.PositiveIntegerField(default=0)
    price_sent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    amount_received = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.id}"
