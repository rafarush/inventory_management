from django.forms import ModelForm
from .models import CartStatus


class CartStatusForm(ModelForm):
    class Meta:
        model = CartStatus
        fields = ['status']

    def clean_status(self):
        status = self.cleaned_data['status']
        if status:
            status = status[0].upper() + status[1:] if status[0].isalpha() else status
        return status
