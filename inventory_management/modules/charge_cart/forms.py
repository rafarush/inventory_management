from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventory_management.models import ChargeCart
from inventory_management.modules.product.models import Product


class ChargeCartAdminForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = ['product', 'amount_sent', 'price_sent', ]

    from django import forms
    from .models import ChargeCart, Product

    class ChargeCartForm(forms.ModelForm):
        class Meta:
            model = ChargeCart
            fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(amount__gt=0)

    def clean_amount_sent(self):
        amount_sent = self.cleaned_data['amount_sent']
        product = self.cleaned_data['product']
        if amount_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        if amount_sent > product.amount:
            raise ValidationError('The amount sent cannot be greater than the amount .'+f"{product.amount}" +'.')
        return amount_sent

    def clean_price_sent(self):
        price_sent = self.cleaned_data['price_sent']
        if price_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        return price_sent


class ChargeCartUpdateForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = ['amount_sent', 'price_sent']

    def clean_amount_sent(self):
        amount_sent = self.cleaned_data['amount_sent']
        product = self.instance.product
        if amount_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        if amount_sent > product.amount:
            raise ValidationError('The amount sent cannot be greater than the amount .'+f"{product.amount}" +'.')
        return amount_sent

    def clean_price_sent(self):
        price_sent = self.cleaned_data['price_sent']
        if price_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        return price_sent


class ChargeCartFinishForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = ['amount_received', 'revenue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_received'].initial = self.instance.amount_received or 0
        self.fields['revenue'].initial = self.instance.revenue or 0

    def clean_revenue(self):
        revenue = self.cleaned_data.get('revenue')
        if revenue is None:
            revenue = 0
        return revenue

    def clean_amount_received(self):
        amount_received = self.cleaned_data['amount_received']
        amount_sent = self.instance.amount_sent
        if amount_received is None:
            amount_received = 0
            return amount_received
        if amount_received < 0:
            raise ValidationError('Price must be greater than 0')
        if amount_received > amount_sent:
            raise ValidationError('The amount received cannot be greater than the amount that comes out.')
        return amount_received
