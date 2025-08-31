from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from inventory_management.modules.custom_user.models import CustomUser


def activate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Convertir bytes a string
        user = CustomUser.objects.get(pk=uid)           # Buscar usuario por UUID string
        if user is not None and default_token_generator.check_token(user, token):
            user.is_confirmed = True
            user.save()
            messages.success(request, 'Correo confirmado correctamente.')
            return redirect('login')
        else:
            messages.error(request, 'El enlace no es válido o expiró.')
            return redirect('login')
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        messages.error(request, 'El enlace no es válido o expiró.')
        return redirect('login')
