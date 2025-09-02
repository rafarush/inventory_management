from django.db import models


class CartStatus(models.Model):
    status = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        verbose_name="Cart Status"
    )

    def __str__(self):
        return f"Cart Status: {self.id}"
