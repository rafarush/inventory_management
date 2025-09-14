from django import forms
from django.core.exceptions import ValidationError
from inventory_management.modules.product.models import Product
from inventory_management.modules.wastage_record.models import WastageRecord
from django.utils.translation import gettext_lazy as _


class WastageRecordForm(forms.ModelForm):
    class Meta:
        model = WastageRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar productos solo con stock > 0 para el campo 'product'
        self.fields['product'].queryset = Product.objects.filter(amount__gt=0)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data['product']
        if quantity <= 0:
            raise ValidationError(_("The quantity must be greater than 0"))
        if product.amount < quantity:
            raise ValidationError(_("The quantity cannot be greater than the current stock"))
        return quantity
