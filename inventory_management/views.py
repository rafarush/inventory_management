from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from inventory_management.models import Product, Worker, Cart  # ajusta según tus modelos

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos datos de resumen
        context['total_products'] = Product.objects.count()
        context['total_workers'] = Worker.objects.count()
        context['total_carts'] = Cart.objects.count()
        return context

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)

def error_403(request, exception):
    return render(request, "errors/403.html", status=403)

def error_400(request, exception):
    return render(request, "errors/400.html", status=400)
