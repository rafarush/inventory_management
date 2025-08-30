from django.contrib.auth.forms import UserCreationForm

from inventory_management.modules.custom_user.models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
