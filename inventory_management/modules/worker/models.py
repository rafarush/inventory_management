from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel


class Worker(BaseModel):
    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("trabajando", "Trabajando"),
    ]
    id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        verbose_name="ID"
    )
    name = models.CharField(max_length=100, verbose_name="name")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="salary")
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="phone"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendiente",
        verbose_name="status",
        editable=False,
    )

    def __str__(self):
        return f"{self.name} ({self.id})"
