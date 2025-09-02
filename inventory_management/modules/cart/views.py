from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from inventory_management.models import Cart
from inventory_management.modules.cart.forms import CartForm


class CartListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cart
    context_object_name = 'carts'
    template_name = 'cart/cart_list.html'
    permission_required = 'inventory_management.view_cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = CartForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class CartCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cart
    success_url = reverse_lazy('cart_list')
    template_name = 'cart/cart_form.html'
    form_class = CartForm
    permission_required = 'inventory_management.add_cart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    context_object_name = 'cart'
    template_name = 'cart/cart_detail.html'


class CartDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cart
    template_name = 'cart/cart_confirm_delete.html'
    success_url = reverse_lazy('cart_list')
    permission_required = 'inventory_management.delete_cart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class CartUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cart
    form_class = CartForm
    template_name = 'cart/cart_form.html'
    success_url = reverse_lazy('cart_list')
    permission_required = 'inventory_management.change_cart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")
