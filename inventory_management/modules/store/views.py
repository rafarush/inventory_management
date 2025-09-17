from django.views.generic import DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Store
from .forms import StoreForm


class StoreMixin:

    def get_object(self, queryset=None):
        obj = Store.objects.first()
        if not obj:
            obj = Store.objects.create()  # se crea automáticamente
        return obj


class StoreDetailView(LoginRequiredMixin, PermissionRequiredMixin, StoreMixin, DetailView):
    model = Store
    template_name = "store/store_detail.html"
    context_object_name = "store"
    permission_required = "inventory_management.view_store"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


class StoreUpdateView(LoginRequiredMixin, PermissionRequiredMixin, StoreMixin, UpdateView):
    model = Store
    form_class = StoreForm
    template_name = "store/store_form.html"
    success_url = reverse_lazy("store_detail")
    permission_required = "inventory_management.change_store"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()
