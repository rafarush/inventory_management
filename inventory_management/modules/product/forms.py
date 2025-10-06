from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _  # ✅ Import necesario
from inventory_management.models import Product


class ProductAdminForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError(_('The price must be greater than 0.'))
        return price

    def clean_id(self):
        id = self.cleaned_data.get('id')
        if id:
            # Si el primer carácter es una letra, ponerlo en mayúscula
            id = id[0].upper() + id[1:] if id[0].isalpha() else id
        return id

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise ValidationError(_('The amount cannot be negative.'))
        return amount


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['price', 'unit', 'amount']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError(_('The price must be greater than 0.'))
        return price

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise ValidationError(_('The amount cannot be negative.'))
        return amount
