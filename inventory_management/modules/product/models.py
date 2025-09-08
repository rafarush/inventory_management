from django.db import models

from inventory_management.modules.base_model.base_model import BaseModel
from inventory_management.modules.store.models import Store


def get_default_store():
    store, created = Store.objects.get_or_create(
        defaults={"name": "Almacén Principal"}
    )
    return store.id


class Product(BaseModel):
    id = models.CharField(primary_key=True, unique=True, max_length=50, )
    unit = models.CharField(max_length=20, default="N/A")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
        editable=False,
        default=get_default_store
    )

    def save(self, *args, **kwargs):
        if not self.store_id:
            store = Store.objects.first()
            if not store:
                store = Store.objects.create(name="Almacén Principal")
            self.store = store
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id
