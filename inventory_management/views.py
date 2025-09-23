from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import TemplateView


# Create your views here.
class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    redirect_field_name = 'next'


