from django.db import models

class Cart(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        verbose_name="Cart ID"
    )

    def __str__(self):
        return f"Cart {self.id}"
