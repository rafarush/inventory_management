from django.views.generic import DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect
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
    permission_required = "store.view_store"


class StoreUpdateView(LoginRequiredMixin, PermissionRequiredMixin, StoreMixin, UpdateView):
    model = Store
    form_class = StoreForm
    template_name = "store/store_form.html"
    success_url = reverse_lazy("store_detail")
    permission_required = "store.change_store"
