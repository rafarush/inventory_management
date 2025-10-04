from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from inventory_management.models import Product
from inventory_management.modules.product.forms import ProductAdminForm, ProductUpdateForm


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/product_list.html'
    permission_required = 'inventory_management.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductAdminForm()
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


# ------------------------- CREATE -------------------------
class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductAdminForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory_management.add_product'

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = {
            'form': form,
            'action_url': reverse_lazy('product_create')
        }
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"success": True, "html": html})
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors})
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


# ------------------------- UPDATE -------------------------
class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory_management.change_product'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Selección de formulario según grupo
        if request.user.groups.filter(name='Administrators').exists():
            self.form_class = ProductAdminForm

        form = self.get_form()
        context = {
            'form': form,
            'action_url': reverse_lazy('product_update', kwargs={'pk': self.object.pk})
        }
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"success": True, "html": html})
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors})
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


# ------------------------- DETAIL -------------------------
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_detail.html'
    permission_required = 'inventory_management.view_product'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(self.template_name, context, request=self.request)
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, "product/product_detail.html", context)
        return super().get(request, *args, **kwargs)


# ------------------------- DELETE -------------------------
class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory_management.delete_product'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            obj = self.get_object()
            html = render_to_string(self.template_name, {'product': obj, 'action_url': self.request.path},
                                    request=request)
            return JsonResponse({'success': True, 'html': html})
        return super().get(request, *args, **kwargs)
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()
