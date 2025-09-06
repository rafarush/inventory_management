from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel


class Cart(BaseModel):
    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("trabajando", "Trabajando"),
    ]
    id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        verbose_name="Cart ID"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendiente",
        verbose_name="status"
    )
    def __str__(self):
        return f"Cart {self.id}"
