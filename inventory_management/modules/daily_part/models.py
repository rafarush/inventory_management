import uuid
from django.db import models
from inventory_management.modules.base_model.base_model import BaseModel


class DailyPart(BaseModel):
    STATUS_CHOICES = [
        ("trabajando", "Trabajando"),
        ("finalizado", "Finalizado"),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    date = models.DateField(auto_now_add=True, unique=True, editable=False)
    money_return_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable= False)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable= False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="trabajando",
        verbose_name="status"
    )

    def __str__(self):
        return f"DailyPart: {self.id} - Date: {self.date} - Status: {self.status}"
