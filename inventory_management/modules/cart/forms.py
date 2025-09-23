from django.forms import ModelForm
from .models import Cart
from django import forms


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_id(self):
        id = self.cleaned_data['id']
        if id:
            id = id[0].upper() + id[1:] if id[0].isalpha() else id
        return id
