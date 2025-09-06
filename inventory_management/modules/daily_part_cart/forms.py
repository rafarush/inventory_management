from django import forms
from inventory_management.modules.daily_part_cart.models import DailyPartCart

class DailyPartCartForm(forms.ModelForm):
    class Meta:
        model = DailyPartCart
        fields = ['worker', 'cart', 'worker_payment']
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-select'}),
            'cart': forms.Select(attrs={'class': 'form-select'}),
            'worker_payment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }
