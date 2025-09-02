from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from inventory_management.models import CartStatus
from inventory_management.modules.cart_status.forms import CartStatusForm


class CartStatusListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CartStatus
    context_object_name = 'cart_status_list'
    template_name = 'cart_status/cart_status_list.html'
    permission_required = 'inventory_management.view_cart_status'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = CartStatusForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class CartStatusCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CartStatus
    success_url = reverse_lazy('cart_status_list')
    template_name = 'cart/cart_form.html'
    form_class = CartStatusForm
    permission_required = 'inventory_management.add_cart_status'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class CartStatusDetailView(LoginRequiredMixin, DetailView):
    model = CartStatus
    context_object_name = 'cart_status'
    template_name = 'cart_status/cart_status_detail.html'


class CartStatusDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CartStatus
    template_name = 'cart_status/cart_status_confirm_delete.html'
    success_url = reverse_lazy('cart_status_list')
    permission_required = 'inventory_management.delete_cart_status'
    context_object_name = 'cart_status'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class CartStatusUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CartStatus
    form_class = CartStatusForm
    template_name = 'cart_status/cart_status_form.html'
    success_url = reverse_lazy('cart_status_list')
    permission_required = 'inventory_management.change_cart_status'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")
