import uuid

from django.db import models
from django.core.exceptions import ValidationError


class Store(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100, default="Almacén Principal")

    own_money = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    money_business = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    percent = models.DecimalField(max_digits=10, decimal_places=2, default=30, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and Store.objects.exists():
            raise ValidationError("Solo puede existir un almacén.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
