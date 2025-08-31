from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import CreateView

from djangoProject import settings
from .forms import SignUpForm


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'auth/logout.html'
    success_url = reverse_lazy('auth/login/')
    next_page = reverse_lazy('index')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'auth/signup.html'

    def form_valid(self, form):
        print("llego a guardar el form")
        user = form.save(commit=False)
        user.is_confirmed = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print("uid user antes")
        print(uid)
        print("token user antes")
        print(token)
        current_site = get_current_site(self.request)
        mail_subject = 'Confirma tu correo'
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        }
        print("antes del email")
        user.send_email(mail_subject, 'emails/email_confirmation_template.html', context)
        print("despues del email")

        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form invalid:", form.errors)
        return super().form_invalid(form)

