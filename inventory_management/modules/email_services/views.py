from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model


def activate_email(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_confirmed = True
        user.save()
        messages.success(request, 'Correo confirmado correctamente.')
        return redirect('auth/login/')
    else:
        messages.error(request, 'El enlace no es válido o expiró.')
        return redirect('auth/signup/')
