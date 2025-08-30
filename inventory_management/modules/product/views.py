from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from inventory_management.models import Product
from inventory_management.modules.product.forms import ProductAdminForm, ProductAgentForm


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/product_list.html'
    permission_required = 'inventory_management.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = ProductAdminForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'product/product_form.html'
    form_class = ProductAdminForm
    permission_required = 'inventory_management.add_product'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_detail.html'


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory_management.delete_product'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductAdminForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory_management.change_product'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Administrators').exists():
            self.form_class = ProductAdminForm
        # elif request.user.groups.filter(name='Agents').exists():
        #     self.form_class = UpdatedProductForm
        # else:
        #     raise PermissionDenied("You do not have permission to perform this action.")

        return super().dispatch(request, *args, **kwargs)
