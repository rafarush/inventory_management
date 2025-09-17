from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import TemplateView


# Create your views here.
class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(name='Managers')

        # Permisos del grupo
        for perm in group.permissions.all():
            print(perm.codename)
        return self.render_to_response(self.get_context_data())


