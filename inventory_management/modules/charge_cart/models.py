import uuid
from decimal import Decimal
from django.db import models
from inventory_management.modules.base_model.base_model import BaseModel
from inventory_management.modules.daily_part_cart.models import DailyPartCart
from inventory_management.modules.product.models import Product  # ajusta la ruta según tu proyecto

class ChargeCart(BaseModel):
    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("finalizado", "Finalizado"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="charges")
    amount_sent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    price_sent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    revenue_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    money_returned = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    money_invested = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendiente")
    daily_part_cart = models.ForeignKey(DailyPartCart, on_delete=models.CASCADE, related_name="charge_carts", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Coalesce None a Decimal('0.00')
        amount_sent = self.amount_sent or Decimal('0.00')
        amount_received = self.amount_received or Decimal('0.00')
        price_sent = self.price_sent or Decimal('0.00')
        product_price = getattr(self.product, 'price', Decimal('0.00'))
        current_stock = getattr(self.product, 'amount', Decimal('0.00'))

        # Calcula revenue y revenue_total
        self.revenue = price_sent - product_price
        self.revenue_total = (amount_sent - amount_received) * self.revenue

        # Revertir efecto antiguo si existe
        if self.pk:
            old = ChargeCart.objects.filter(pk=self.pk).only('amount_sent', 'amount_received').first()
            if old:
                old_sent = old.amount_sent or Decimal('0.00')
                old_recv = old.amount_received or Decimal('0.00')
                current_stock += old_sent - old_recv

        # Aplicar los movimientos actuales
        current_stock = current_stock - amount_sent + amount_received
        self.product.amount = current_stock

        self.product.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.amount_sent:
            self.product.amount += self.amount_sent

        self.product.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"{self.product.id}"
