from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from inventory_management.modules.daily_part.forms import DailyPartForm
from inventory_management.modules.daily_part.models import DailyPart
from django.utils.translation import gettext_lazy as _


class DailyPartListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DailyPart
    context_object_name = 'daily_parts'
    template_name = 'daily_part/daily_part_list.html'
    permission_required = 'inventory_management.view_dailypart'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class DailyPartCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DailyPart
    success_url = reverse_lazy('daily_part_list')
    permission_required = 'inventory_management.add_dailypart'

    def form_valid(self, form):
        today = now().date()
        daily_part = DailyPart.objects.filter(date=today).first()

        if daily_part:
            if daily_part.status == "finalizado":
                form.add_error(None, "El Daily Part de hoy ya está finalizado y no se pueden agregar más registros.")
                return self.form_invalid(form)
        else:
            daily_part = DailyPart.objects.create(date=today)

        self.object = form.save(commit=False)
        self.object.daily_part = daily_part
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class DailyPartDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DailyPart
    context_object_name = 'daily_part'
    template_name = 'daily_part/daily_part_detail.html'
    permission_required = 'inventory_management.view_dailypart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        daily_part_carts = self.get_object().daily_part_carts.all()
        context["daily_part_carts"] = daily_part_carts
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# class DailyPartUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = DailyPart
#     form_class = DailyPartForm
#     template_name = 'daily_part/daily_part_form.html'
#     success_url = reverse_lazy('daily_part_list')
#     permission_required = 'inventory_management.change_dailypart'
#
#     def handle_no_permission(self):
#         raise PermissionDenied("You do not have permission to perform this action.")


# class DailyPartDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = DailyPart
#     template_name = 'daily_part/daily_part_confirm_delete.html'
#     success_url = reverse_lazy('daily_part_list')
#     context_object_name = 'daily_part'
#     permission_required = 'inventory_management.delete_dailypart'
#
#     def __init__(self, **kwargs):
#         super().__init__(kwargs)
#         self.object = None
#
#     def handle_no_permission(self):
#         raise PermissionDenied("You do not have permission to perform this action.")


# def validate_daily_part_finalizado(request):
#     today = now().date()
#     daily_part = DailyPart.objects.filter(date=today).first()
#     finalizado = daily_part.status == "finalizado" if daily_part else False
#     return JsonResponse({"finalizado": finalizado})


class DailyPartFinishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'inventory_management.change_dailypart'

    def post(self, request, pk):
        daily_part = get_object_or_404(DailyPart, pk=pk)

        # Verificar que todos los daily part carts estén finalizados
        all_finalized = all(dp.status == "finalizado" for dp in daily_part.daily_part_carts.all())
        if not all_finalized:
            messages.error(request, _("Cannot finish Daily Part: there are pending daily part carts."))
            return redirect("daily_part_list")

        daily_part.status = "finalizado"
        daily_part.save(update_fields=["status"])

        messages.success(request, _("Daily Part finished successfully"))
        return redirect("daily_part_list")
