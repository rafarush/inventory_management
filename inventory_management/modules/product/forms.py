from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventory_management.models import Product


class ProductAdminForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price

    def clean_id(self):
        id = self.cleaned_data['id']
        if id:
            # Si el primer carácter es una letra, ponerlo en mayúscula
            id = id[0].upper() + id[1:] if id[0].isalpha() else id
        return id


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['price', 'unit']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price

    def clean_id(self):
        id = self.cleaned_data['id']
        if id:
            # Si el primer carácter es una letra, ponerlo en mayúscula
            id = id[0].upper() + id[1:] if id[0].isalpha() else id
        return id
