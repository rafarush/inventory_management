from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from inventory_management.models import ProductCategory
from inventory_management.modules.product_category.forms import ProductCategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ProductCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProductCategory
    context_object_name = 'product_categories'
    template_name = 'product_category/product_category_list.html'
    permission_required = 'inventory_management.view_productcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = ProductCategoryForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied('You do not have permission to perform this action.')


class ProductCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')
    template_name = 'product_category/product_category_form.html'
    form_class = ProductCategoryForm
    permission_required = 'inventory_management.create_productcategory'

    def handle_no_permission(self):
        raise PermissionDenied('You do not have permission to perform this action.')


class ProductCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductCategory
    context_object_name = 'product_category'
    template_name = 'product_category/product_category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('product_category_list')
    permission_required = 'inventory_management.change_productcategory'

    def handle_no_permission(self):
        raise PermissionDenied('You do not have permission to perform this action.')


class ProductCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'product_category/product_category_confirm_delete.html'
    success_url = reverse_lazy('product_category_list')
    permission_required = 'inventory_management.delete_productcategory'

    def handle_no_permission(self):
        raise PermissionDenied('You do not have permission to perform this action.')
