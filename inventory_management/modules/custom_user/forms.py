from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from inventory_management.models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number1', 'phone_number2',
                  'email', 'groups']


class CustomUserSetPasswordForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number1', 'phone_number2', 'groups']
        exclude = ['password1', 'password2']
