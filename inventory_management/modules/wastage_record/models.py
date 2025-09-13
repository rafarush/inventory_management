import uuid
from inventory_management.modules.base_model.base_model import BaseModel
from django.db import models
from decimal import Decimal

from inventory_management.modules.product.models import Product


class WastageRecord(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(auto_now=False, auto_now_add=True, editable=False)

    # def save(self, *args, **kwargs):
    #     current_stock = getattr(self.product, 'amount', Decimal('0.00'))
    #     quantity = self.quantity or Decimal('0.00')
    #
    #     self.product.amount = current_stock - quantity
    #     self.product.save()
    #
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     current_stock = getattr(self.product, 'amount', Decimal('0.00'))
    #     quantity = self.quantity or Decimal('0.00')
    #
    #     self.product.amount = current_stock + quantity
    #
    #     self.product.save()
    #     super().delete(*args, **kwargs)
