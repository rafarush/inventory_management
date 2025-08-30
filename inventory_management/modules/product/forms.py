from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventory_management.models import Product


class ProductAdminForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'class': 'fixed-size-description'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            exists = Product.objects.exclude(pk=instance.pk).filter(name=name).exists()
        else:
            exists = Product.objects.filter(name=name).exists()

        if exists:
            raise ValidationError('This product already exists')
        return name

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock <= 0:
            raise ValidationError('Stock must be greater than 0')
        return stock


class ProductAgentForm(ModelForm):
    class Meta:
        model = Product
        fields = ['price']

    def clean_price(self):
        price = self.cleaned_data['price']
        old_price = Product.objects.get(pk=self.instance.pk).price
        if price <= 0:
            raise ValidationError('Price must be greater than 0')
        elif price < old_price:
            raise ValidationError('The new price must be greater than or equal to the old price: ' + str(old_price))
        return price
