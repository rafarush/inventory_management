from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventory_management.modules.charge_cart.models import ChargeCart
from inventory_management.modules.product.models import Product


class ChargeCartAdminForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = ['product', 'amount_sent', 'price_sent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar productos con stock
        self.fields['product'].queryset = Product.objects.filter(amount__gt=0)

    def clean_amount_sent(self):
        amount_sent = self.cleaned_data['amount_sent']
        product = self.cleaned_data['product']
        if amount_sent <= 0:
            raise ValidationError('The amount sent must be greater than 0.')
        if amount_sent > product.amount:
            raise ValidationError(
                f'The amount sent cannot be greater than the available stock ({product.amount}).'
            )
        return amount_sent

    def clean_price_sent(self):
        price_sent = self.cleaned_data['price_sent']
        if price_sent <= 0:
            raise ValidationError('The price must be greater than 0.')
        return price_sent


# ✅ Este es el formulario que usas en la vista create/update
class ChargeCartForm(forms.ModelForm):
    class Meta:
        model = ChargeCart
        exclude = ['daily_part_cart']  # se asigna automáticamente en la vista


class ChargeCartUpdateForm(ModelForm):
    class Meta:
        model = ChargeCart
        fields = ['amount_sent', 'price_sent']

    def clean_amount_sent(self):
        amount_sent = self.cleaned_data['amount_sent']
        product = self.instance.product
        if amount_sent <= 0:
            raise ValidationError('The amount sent must be greater than 0.')
        if amount_sent > product.amount:
            raise ValidationError(
                f'The amount sent cannot be greater than the available stock ({product.amount}).'
            )
        return amount_sent

    def clean_price_sent(self):
        price_sent = self.cleaned_data['price_sent']
        if price_sent <= 0:
            raise ValidationError('The price must be greater than 0.')
        return price_sent


from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import ChargeCart

class ChargeCartFinishForm(ModelForm):
    amount_received = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.TextInput(attrs={'type': 'text'}),  # permite vacío
        initial=Decimal('0.00')
    )

    class Meta:
        model = ChargeCart
        fields = ['amount_received']

    def clean_amount_received(self):
        value = self.cleaned_data.get('amount_received')
        if value in (None, ''):
            value = Decimal('0.00')
        amount_sent = self.instance.amount_sent or Decimal('0.00')

        if value < 0:
            raise ValidationError('The amount received must be >= 0.')
        if value > amount_sent:
            raise ValidationError('The amount received cannot be greater than the amount sent.')
        return value
