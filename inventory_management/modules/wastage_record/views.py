import math

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.db.models import Case, When, Value, IntegerField
from decimal import Decimal
from inventory_management.modules.wastage_record.forms import WastageRecordForm
from inventory_management.modules.wastage_record.models import WastageRecord


class WastageRecordListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = WastageRecord
    context_object_name = 'records'
    template_name = 'wastage_records/wastage_records_list.html'
    permission_required = 'wastage_record.view_wastagerecords'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def get_queryset(self):
        qs = super().get_queryset()
        # Ordenar por fecha descendente (las más actuales primero)
        qs = qs.order_by('-date')
        # Orden dinámico según parámetro GET
        order_by = self.request.GET.get('order_by')
        if order_by and order_by != '-date':
            qs = qs.order_by(order_by)
        return qs


class WastageRecordCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = WastageRecord
    form_class = WastageRecordForm
    template_name = 'wastage_records/wastage_record_form.html'
    success_url = reverse_lazy('wastage_record_list')
    permission_required = 'wastage_record.add_wastagerecord'

    def form_valid(self, form):
        # Guardamos la instancia sin hacer commit para poder acceder a ella
        self.object = form.save(commit=False)

        # Reducimos el stock del producto
        current_stock = getattr(self.object.product, 'amount', Decimal('0.00'))
        quantity = self.object.quantity or Decimal('0.00')
        self.object.product.amount = current_stock - quantity
        self.object.product.save()

        # Guardamos finalmente la instancia de WastageRecord
        self.object.save()

        return super().form_valid(form)

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class WastageRecordDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = WastageRecord
    template_name = 'wastage_records/wastage_record_confirm_delete.html'
    success_url = reverse_lazy('wastage_record_list')
    context_object_name = 'wastage_record'
    permission_required = 'wastage_record.delete_wastagerecord'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Suma el stock antes de eliminar el registro
        current_stock = getattr(self.object.product, 'amount', Decimal('0.00'))
        quantity = self.object.quantity or Decimal('0.00')

        self.object.product.amount = current_stock + quantity
        self.object.product.save()

        return super().post(request, *args, **kwargs)

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class WastageRecordUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = WastageRecord
    form_class = WastageRecordForm
    template_name = 'wastage_records/wastage_record_form.html'
    success_url = reverse_lazy('wastage_record_list')
    permission_required = 'wastage_record.change_wastagerecord'

    def form_valid(self, form):
        old_object = self.get_object()
        old_quantity = old_object.quantity or Decimal('0.00')

        new_object = form.save(commit=False)
        new_quantity = new_object.quantity or Decimal('0.00')

        quantity_diff = abs(new_quantity - old_quantity)

        # Actualizar stock restando la diferencia
        current_stock = getattr(new_object.product, 'amount', Decimal('0.00'))
        if new_quantity > old_quantity:
            new_object.product.amount = current_stock - quantity_diff
        else:
            new_object.product.amount = current_stock + quantity_diff

        new_object.product.save()

        # Guardar el registro actualizado
        new_object.save()

        return super().form_valid(form)

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")