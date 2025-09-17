from django import forms
from django.core.exceptions import ValidationError
from inventory_management.modules.product.models import Product
from inventory_management.modules.wastage_record.models import WastageRecord
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class WastageRecordForm(forms.ModelForm):
    class Meta:
        model = WastageRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar productos solo con stock > 0 para el campo 'product'
        self.fields['product'].queryset = Product.objects.filter(
            Q(amount__gt=0) | Q(wastagerecord__isnull=False)
        ).distinct()

    def clean_quantity(self):
        new_quantity = self.cleaned_data['quantity']
        product = self.cleaned_data['product']

        if new_quantity <= 0:
            raise ValidationError(_("The quantity must be greater than 0"))

        # Stock actual del producto en BD
        current_stock = product.amount

        # Cantidad previa en el registro original (antes de editar)
        previous_quantity = self.instance.quantity if self.instance.pk else 0

        # Stock disponible para asignar, considerando la cantidad editada
        available_stock = current_stock + previous_quantity

        if new_quantity > available_stock:
            raise ValidationError(_("The quantity cannot be greater than the current stock available"))

        return new_quantity

