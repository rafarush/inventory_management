from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "percent", "own_money", "money_business"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),  # fijo
            "own_money": forms.NumberInput(attrs={"class": "form-control"}),
            "money_business": forms.NumberInput(attrs={"class": "form-control"}),
            "percent": forms.NumberInput(attrs={"class": "form-control"}),
        }
