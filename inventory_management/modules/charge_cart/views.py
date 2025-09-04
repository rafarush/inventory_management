# inventory_management/modules/charge_cart/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from inventory_management.modules.charge_cart.models import ChargeCart
from inventory_management.modules.charge_cart.forms import ChargeCartAdminForm, ChargeCartUpdateForm, \
    ChargeCartFinishForm
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpResponseRedirect


class ChargeCartListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ChargeCart
    context_object_name = 'charge_cart_list'
    template_name = 'charge_cart/charge_cart_list.html'
    permission_required = 'charge_cart.view_chargecart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChargeCartAdminForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def get_queryset(self):
        return ChargeCart.objects.annotate(
            status_order=Case(
                When(status='pendiente', then=Value(0)),
                When(status='finalizado', then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('status_order')


class ChargeCartCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ChargeCart
    form_class = ChargeCartAdminForm
    template_name = 'charge_cart/charge_cart_form.html'
    success_url = reverse_lazy('charge_cart_list')
    permission_required = 'charge_cart.add_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ChargeCartDetailView(LoginRequiredMixin, DetailView):
    model = ChargeCart
    context_object_name = 'charge_cart'
    template_name = 'charge_cart/charge_cart_detail.html'


class ChargeCartDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ChargeCart
    template_name = 'charge_cart/charge_cart_confirm_delete.html'
    success_url = reverse_lazy('charge_cart_list')
    context_object_name = 'charge_cart'
    permission_required = 'charge_cart.delete_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ChargeCartUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ChargeCart
    form_class = ChargeCartUpdateForm
    template_name = 'charge_cart/charge_cart_form.html'
    success_url = reverse_lazy('charge_cart_list')
    permission_required = 'charge_cart.change_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ChargeCartFinishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ChargeCart
    form_class = ChargeCartFinishForm
    template_name = 'charge_cart/charge_cart_form.html'
    success_url = reverse_lazy('charge_cart_list')
    permission_required = 'charge_cart.change_chargecart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")

    def form_valid(self, form):
        instance = form.save(commit=False)

        for field_name in form.fields:
            value = getattr(instance, field_name, None)
            if value in [None, '', 0]:
                form.add_error(field_name, "This field is required to complete.")
                return self.form_invalid(form)

        instance.money_returned = (instance.price_sent * (instance.amount_sent - instance.amount_received))
        instance.revenue_total =  (instance.revenue *  (instance.amount_sent - instance.amount_received))

        instance.status = "finalizado"
        instance.save()

        return HttpResponseRedirect(self.get_success_url())
