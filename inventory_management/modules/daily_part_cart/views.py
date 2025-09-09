from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from inventory_management.modules.daily_part_cart.models import DailyPartCart
from inventory_management.modules.daily_part_cart.forms import DailyPartCartForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

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
    context_object_name = 'daily_part_cart'
    permission_required = 'inventory_management.delete_dailypartcart'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Borrado lógico de todos los ChargeCart asociados
        for charge in self.object.charge_carts.all():
            charge.delete()  # esto aplica borrado lógico si tu modelo lo implementa

        # Cambiar estado del worker y cart a pendiente
        self.object.worker.status = "pendiente"
        self.object.worker.save(update_fields=["status"])

        self.object.cart.status = "pendiente"
        self.object.cart.save(update_fields=["status"])

        # Borrado lógico del DailyPartCart
        self.object.delete()  # SafeDelete u otra librería hará borrado lógico

        messages.success(request, "Parte diario y sus cargas asociadas eliminados correctamente.")
        return redirect(self.success_url)

class DailyPartCartFinishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'inventory_management.change_dailypartcart'

    def post(self, request, pk):
        daily_part = get_object_or_404(DailyPartCart, pk=pk)

        # Verificar que todos los charge_cart estén finalizados
        all_finalized = all(cc.status == "finalizado" for cc in daily_part.charge_carts.all())
        if not all_finalized:
            messages.error(request, "No puedes finalizar: hay ChargeCart pendientes.")
            return redirect("daily_part_cart_list")

        # ---- Cálculos de totales ----
        money_return_total = sum(cc.money_returned or 0 for cc in daily_part.charge_carts.all())
        revenue_total = sum(cc.revenue_total or 0 for cc in daily_part.charge_carts.all())
        net_profit = revenue_total - (daily_part.worker_payment or 0)

        # Guardar en el DailyPartCart
        daily_part.money_return_total = money_return_total
        daily_part.revenue = revenue_total
        daily_part.net_profit = net_profit
        daily_part.status = "finalizado"
        daily_part.save(update_fields=["money_return_total", "revenue", "net_profit", "status"])

        # Cambiar estado del worker y cart
        daily_part.worker.status = "pendiente"
        daily_part.worker.save(update_fields=["status"])

        daily_part.cart.status = "pendiente"
        daily_part.cart.save(update_fields=["status"])

        messages.success(request, "Parte diario finalizado correctamente.")
        return redirect("daily_part_cart_list")
