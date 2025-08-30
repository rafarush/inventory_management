from django.db import models


class ProductCategory(models.Model):
    category = models.CharField(primary_key=True,max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.category

