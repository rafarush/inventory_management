from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from inventory_management.models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number1', 'phone_number2',
                  'first_name', 'last_name', 'email', 'groups']

    def clean_id_number(self):
        id = self.cleaned_data['id_number']
        if not id and len(id) != 11:
            raise ValidationError(f'Invalid ID Number, the ID Number must have 11 characters: {id}')

        if not id.isdigit():
            raise ValidationError(f'Invalid ID Number, the ID Number must have only numbers: {id}')

        try:
            date = datetime.strptime(id[:6], "%y%m%d")
            return id
        except ValueError:
            raise ValidationError(f'Invalid ID Number, invalid date of birth in the ID Number: {id}')
