# inventory_management/modules/charge_cart/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from inventory_management.modules.charge_cart.models import ChargeCart
from inventory_management.modules.charge_cart.forms import (
    ChargeCartAdminForm, ChargeCartUpdateForm, ChargeCartFinishForm
)
from inventory_management.modules.daily_part_cart.models import DailyPartCart


# 🔹 LISTA DE CHARGECART
class ChargeCartListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ChargeCart
    context_object_name = 'charge_cart_list'
    template_name = 'charge_cart/charge_cart_list.html'
    permission_required = 'charge_cart.view_chargecart'

    def get_queryset(self):
        qs = super().get_queryset()
        daily_part_cart_id = self.kwargs.get('daily_part_cart_id')

        if daily_part_cart_id:  # filtrar si viene desde un DailyPartCart
            qs = qs.filter(daily_part_cart_id=daily_part_cart_id)

        # ordenar si viene en GET
        order_by = self.request.GET.get('order_by')
        if order_by == 'status':
            qs = qs.annotate(
                status_order=Case(
                    When(status='pendiente', then=Value(0)),
                    When(status='finalizado', then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            ).order_by('status_order')
        elif order_by in [
            'product', 'amount_sent', 'price_sent',
            'amount_received', 'revenue', 'revenue_total', 'money_returned'
        ]:
            qs = qs.order_by(order_by if order_by != 'product' else 'product')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        daily_part_cart_id = self.kwargs.get('daily_part_cart_id')

        if daily_part_cart_id:
            context['daily_part_cart'] = get_object_or_404(DailyPartCart, pk=daily_part_cart_id)

        context['form'] = ChargeCartAdminForm()
        context['current_order'] = self.request.GET.get('order_by', '')
        context['search_term'] = self.request.GET.get('search', '')
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# 🔹 CREAR CHARGECART
class ChargeCartCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ChargeCart
    form_class = ChargeCartAdminForm
    template_name = 'charge_cart/charge_cart_form.html'
    permission_required = 'charge_cart.add_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def form_valid(self, form):
        # asignar automáticamente el daily_part_cart_id desde la URL si existe
        daily_part_cart_id = self.kwargs.get('daily_part_cart_id')
        if daily_part_cart_id:
            form.instance.daily_part_cart_id = daily_part_cart_id
        return super().form_valid(form)

    def get_success_url(self):
        daily_part_cart_id = self.kwargs.get('daily_part_cart_id')
        if daily_part_cart_id:
            return reverse_lazy('charge_cart_list_by_daily', kwargs={'daily_part_cart_id': daily_part_cart_id})
        return reverse_lazy('charge_cart_list')


# 🔹 DETALLE
class ChargeCartDetailView(LoginRequiredMixin, DetailView):
    model = ChargeCart
    context_object_name = 'charge_cart'
    template_name = 'charge_cart/charge_cart_detail.html'


# 🔹 ELIMINAR
class ChargeCartDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ChargeCart
    template_name = 'charge_cart/charge_cart_confirm_delete.html'
    success_url = reverse_lazy('charge_cart_list')
    context_object_name = 'charge_cart'
    permission_required = 'charge_cart.delete_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# 🔹 ACTUALIZAR
class ChargeCartUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ChargeCart
    form_class = ChargeCartUpdateForm
    template_name = 'charge_cart/charge_cart_form.html'
    success_url = reverse_lazy('charge_cart_list')
    permission_required = 'charge_cart.change_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# 🔹 FINALIZAR
class ChargeCartFinishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ChargeCart
    form_class = ChargeCartFinishForm
    template_name = 'charge_cart/charge_cart_form.html'
    #success_url = reverse_lazy('charge_cart_list_by_daily')
    permission_required = 'charge_cart.change_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def form_valid(self, form):
        instance = form.save(commit=False)

        # validación de campos obligatorios
        for field_name in form.fields:
            value = getattr(instance, field_name, None)
            if value in [None, '', 0]:
                form.add_error(field_name, "This field is required to complete.")
                return self.form_invalid(form)

        amount_v=(instance.amount_sent - instance.amount_received)
        instance.money_returned = instance.price_sent * amount_v
        instance.revenue_total = instance.revenue * amount_v
        print("amount_v:", amount_v)
        print("instance.revenue_total:", instance.revenue_total)
        print("instance.money_returned:", instance.money_returned)
        print("instance.amount_received:", instance.amount_received)
        print("instance.amount_sent:", instance.amount_sent)
        instance.status = "finalizado"
        instance.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # Obtén el daily_part_cart_id del ChargeCart actual
        daily_part_cart_id = self.object.daily_part_cart.id
        # Haz el reverse pasando el argumento
        return reverse_lazy('charge_cart_list_by_daily', kwargs={'daily_part_cart_id': daily_part_cart_id})
