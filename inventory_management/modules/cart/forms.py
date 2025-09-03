from django.forms import ModelForm
from .models import Cart


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

    def clean_id(self):
        id = self.cleaned_data['id']
        if id:
            id = id[0].upper() + id[1:] if id[0].isalpha() else id
        return id
