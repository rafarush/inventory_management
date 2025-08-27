from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.
class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')


class CustomLogoutView(LogoutView):
    template_name = 'auth/logout.html'
    next_page = reverse_lazy('index')
