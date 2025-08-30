import uuid

from django.db import models
from inventory_management.modules.product_category.models import ProductCategory


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/product_images', null=True, blank=True)

    def __str__(self):
        return self.name
