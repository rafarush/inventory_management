from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel


class Cart(BaseModel):
    id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        verbose_name="Cart ID"
    )

    def __str__(self):
        return f"Cart {self.id}"
