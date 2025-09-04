from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel


class Product(BaseModel):
    id = models.CharField(primary_key=True, unique=True, max_length=50,)
    unit = models.CharField(max_length=20, default="N/A")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return self.id
