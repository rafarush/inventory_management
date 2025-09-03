from django.db import models


class Worker(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        verbose_name="ID",
        editable=False
    )
    name = models.CharField(max_length=100, verbose_name="name")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="salary")
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="phone"
    )

    def __str__(self):
        return f"{self.name} ({self.id})"
