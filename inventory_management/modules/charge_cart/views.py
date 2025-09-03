# inventory_management/modules/charge_cart/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from inventory_management.modules.charge_cart.models import ChargeCart
from inventory_management.modules.charge_cart.forms import ChargeCartAdminForm, ChargeCartUpdateForm


class ChargeCartListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ChargeCart
    context_object_name = 'charge_cart_list'
    template_name = 'charge_cart/charge_cart_list.html'
    permission_required = 'charge_cart.view_chargecart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChargeCartAdminForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

from django.http import HttpResponseNotAllowed
class ChargeCartCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ChargeCart
    form_class = ChargeCartAdminForm
    template_name = 'charge_cart/charge_cart_form.html'  # se mostrará en /create/
    success_url = reverse_lazy('charge_cart_list')
    permission_required = 'charge_cart.add_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

class ChargeCartDetailView(LoginRequiredMixin, DetailView):
    model = ChargeCart
    context_object_name = 'charge_cart'
    template_name = 'charge_cart/charge_cart_detail.html'


class ChargeCartDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ChargeCart
    template_name = 'charge_cart/charge_cart_confirm_delete.html'
    success_url = reverse_lazy('charge_cart_list')
    context_object_name = 'charge_cart'
    permission_required = 'charge_cart.delete_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ChargeCartUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ChargeCart
    form_class = ChargeCartUpdateForm
    template_name = 'charge_cart/charge_cart_form.html'
    success_url = reverse_lazy('charge_cart_list')
    permission_required = 'charge_cart.change_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")
