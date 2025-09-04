from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel


class ProductCategory(BaseModel):
    category = models.CharField(primary_key=True,max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.category

