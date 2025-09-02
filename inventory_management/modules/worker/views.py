from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Worker
from .forms import WorkerAdminForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# List all workers
class WorkerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Worker
    template_name = 'worker/workers_list.html'
    context_object_name = 'workers'
    permission_required = 'inventory_management.view_worker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = WorkerAdminForm()
        return context

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# Detail view
class WorkerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Worker
    template_name = 'worker/worker_detail.html'
    context_object_name = 'worker'
    permission_required = 'inventory_management.view_worker'


# Create worker
class WorkerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerAdminForm
    template_name = 'worker/worker_form.html'
    success_url = reverse_lazy('worker_list')
    permission_required = 'inventory_management.create_worker'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# Update worker
class WorkerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerAdminForm
    template_name = 'worker/worker_form.html'
    success_url = reverse_lazy('worker_list')
    permission_required = 'inventory_management.change_worker'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


# Delete worker
class WorkerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Worker
    template_name = 'worker/worker_confirm_delete.html'
    success_url = reverse_lazy('worker_list')
    permission_required = 'inventory_management.delete_worker'

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")
