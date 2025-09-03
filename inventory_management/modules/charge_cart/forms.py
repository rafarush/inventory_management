from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventory_management.models import ChargeCart


class ChargeCartAdminForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = '__all__'

    def clean_amount_sent(self):
        amount_sent = self.cleaned_data['amount_sent']
        if amount_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        return amount_sent

    def clean_price_sent(self):
        price_sent = self.cleaned_data['price_sent']
        if price_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        return price_sent

    def clean_amount_received(self):
        amount_received = self.cleaned_data['amount_received']
        if amount_received < 0:
            raise ValidationError('Price must be greater than 0')
        return amount_received

    def clean_revenue(self):
        revenue = self.cleaned_data['revenue']
        if revenue <= 0:
            raise ValidationError('Price must be greater than 0')
        return revenue

    def clean_revenue_total(self):
        revenue_total = self.cleaned_data['revenue_total']
        if revenue_total <= 0:
            raise ValidationError('Price must be greater than 0')
        return revenue_total


class ChargeCartUpdateForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = ['amount_sent']

    def clean_amount_sent(self):
        amount_sent = self.cleaned_data['amount_sent']
        if amount_sent <= 0:
            raise ValidationError('Price must be greater than 0')
        return amount_sent
