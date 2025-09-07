from django import forms

from inventory_management.modules.cart.models import Cart
from inventory_management.modules.daily_part_cart.models import DailyPartCart
from inventory_management.modules.worker.models import Worker


class DailyPartCartForm(forms.ModelForm):
    class Meta:
        model = DailyPartCart
        fields = ['worker', 'cart', 'worker_payment']
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-select'}),
            'cart': forms.Select(attrs={'class': 'form-select'}),
            'worker_payment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo workers y carts con estado pendiente
        self.fields['worker'].queryset = Worker.objects.filter(status="pendiente")
        self.fields['cart'].queryset = Cart.objects.filter(status="pendiente")