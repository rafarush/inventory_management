from django import forms

from inventory_management.modules.daily_part.models import DailyPart


class DailyPartForm(forms.ModelForm):
    class Meta:
        model = DailyPart
        fields = '__all__'