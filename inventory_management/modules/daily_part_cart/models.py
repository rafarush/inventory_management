import uuid
from django.db import models
from inventory_management.modules.base_model.base_model import BaseModel
from inventory_management.modules.cart.models import Cart
from inventory_management.modules.worker.models import Worker


class DailyPartCart(BaseModel):
    STATUS_CHOICES = [
        ("trabajando", "Trabajando"),
        ("finalizado", "Finalizado"),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name="daily_parts"
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="daily_parts"
    )

    money_return_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable= False)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable= False)
    worker_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable= False)

    date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="trabajando",
        verbose_name="status"
    )

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # detecta si es creación
        super().save(*args, **kwargs)

        if is_new:
            self.worker.status = "trabajando"
            self.worker.save(update_fields=["status"])

            self.cart.status = "trabajando"
            self.cart.save(update_fields=["status"])

    def __str__(self):
        return f"DailyPartCart {self.id} - Worker: {self.worker.name} - Cart: {self.cart.id}"
