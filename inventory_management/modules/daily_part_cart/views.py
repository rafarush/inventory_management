from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from inventory_management.modules.daily_part_cart.models import DailyPartCart
from inventory_management.modules.daily_part_cart.forms import DailyPartCartForm


class DailyPartCartListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DailyPartCart
    context_object_name = 'daily_part_carts'
    template_name = 'daily_part_cart/daily_part_cart_list.html'
    permission_required = 'inventory_management.view_dailypartcart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DailyPartCartForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class DailyPartCartCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DailyPartCart
    form_class = DailyPartCartForm
    template_name = 'daily_part_cart/daily_part_cart_form.html'
    success_url = reverse_lazy('daily_part_cart_list')
    permission_required = 'inventory_management.add_dailypartcart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class DailyPartCartDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DailyPartCart
    context_object_name = 'daily_part_cart'
    template_name = 'daily_part_cart/daily_part_cart_detail.html'
    permission_required = 'inventory_management.view_dailypartcart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class DailyPartCartUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DailyPartCart
    form_class = DailyPartCartForm
    template_name = 'daily_part_cart/daily_part_cart_form.html'
    success_url = reverse_lazy('daily_part_cart_list')
    permission_required = 'inventory_management.change_dailypartcart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class DailyPartCartDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DailyPartCart
    template_name = 'daily_part_cart/daily_part_cart_confirm_delete.html'
    success_url = reverse_lazy('daily_part_cart_list')
    context_object_name = 'daily_part_cart'  # <-- Agregado
    permission_required = 'inventory_management.delete_dailypartcart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

