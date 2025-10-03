from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Worker
from .forms import WorkerAdminForm, WorkerUpdateForm
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
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


# Detail view
class WorkerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Worker
    template_name = 'worker/worker_detail.html'
    context_object_name = 'worker'
    permission_required = 'inventory_management.view_worker'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, "worker/worker_detail.html", context)
        return super().get(request, *args, **kwargs)


# Create worker
class WorkerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerAdminForm
    template_name = 'worker/worker_form.html'
    success_url = reverse_lazy('worker_list')
    permission_required = 'inventory_management.add_worker'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = {'form': form}
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # Devuelve solo el HTML del form
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"success": True, "html": html})
        return super().get(request, *args, **kwargs)

# Update worker
class WorkerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = 'worker/worker_form.html'
    success_url = reverse_lazy('worker_list')
    permission_required = 'inventory_management.change_worker'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors}, status=400)
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = {'form': form}
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # Devuelve solo el HTML del form
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"success": True, "html": html})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return super().form_valid(form)


# Delete worker
class WorkerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Worker
    template_name = 'worker/worker_confirm_delete.html'
    success_url = reverse_lazy('worker_list')
    permission_required = 'inventory_management.delete_worker'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(self.template_name, {"worker": self.object}, request=request)
            return HttpResponse(html)
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        """Django DeleteView usa POST para confirmar, aquí redirigimos a delete"""
        return self.delete(request, *args, **kwargs)
