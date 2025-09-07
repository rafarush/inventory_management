import uuid
from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel
from inventory_management.modules.daily_part_cart.models import DailyPartCart
from inventory_management.modules.product.models import Product  # ajusta la ruta según tu proyecto


class ChargeCart(BaseModel):
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
    revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)

    revenue_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True, editable= False)
    money_returned = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True, editable= False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendiente"
    )
    daily_part_cart = models.ForeignKey(
        DailyPartCart,
        on_delete=models.CASCADE,
        related_name="charge_carts",
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.price_sent and self.product and hasattr(self.product, "price"):
            self.revenue = self.price_sent - self.product.price

            if self.amount_sent:
                self.revenue_total = (self.price_sent - self.product.price) * self.amount_sent
            else:
                self.revenue_total = 0
        else:
            self.revenue = 0
            self.revenue_total = 0

        if self.pk and ChargeCart.objects.filter(pk=self.pk).exists():
            old = ChargeCart.objects.get(pk=self.pk)

            self.product.amount += old.amount_sent or 0
            self.product.amount -= old.amount_received or 0

        if self.amount_sent:
            self.product.amount -= self.amount_sent
        if self.amount_received:
            self.product.amount += self.amount_received

        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.amount_sent:
            self.product.amount += self.amount_sent

        self.product.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"{self.product.id}"
