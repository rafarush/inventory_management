from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.models import Permission, Group
from inventory_management.modules.custom_user.forms import CustomUserForm
from inventory_management.models import CustomUser
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect


class CustomUserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'custom_user/custom_user_list.html'
    permission_required = 'inventory_management.view_customuser'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


class CustomUserClientsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'custom_user/custom_user_list.html'
    permission_required = 'inventory_management.view_customuser'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()

    def get_queryset(self):
        if self.request.user.groups.filter(name='Administrators').exists() or self.request.user.groups.filter(
                name='Agents').exists():
            return CustomUser.objects.filter(groups__name='Clients')


class CustomUserCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'custom_user/custom_user_form.html'
    success_url = reverse_lazy('custom_user_list')
    permission_required = 'inventory_management.add_customuser'

    def get_form(self, form_class=CustomUserForm):
        form = super(CustomUserCreate, self).get_form(form_class)
        user = self.request.user
        if user.groups.filter(name='Administrators').exists():
            form.fields['groups'].queryset = Group.objects.all()
        elif user.groups.filter(name='Agents').exists():
            form.fields['groups'].queryset = Group.objects.filter(name='Clients')
        return form

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


class CustomUserDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomUser
    context_object_name = 'user'
    success_url = reverse_lazy('custom_user_list')
    template_name = 'custom_user/custom_user_confirm_delete.html'
    permission_required = 'inventory_management.delete_customuser'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


class CustomUserDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'custom_user/custom_user_detail.html'
    permission_required = 'inventory_management.view_customuser'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


class CustomUserUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'custom_user/custom_user_form.html'
    success_url = reverse_lazy('custom_user_list')
    permission_required = 'inventory_management.change_customuser'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()


class CustomUserDetailsJSON(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'inventory_management.view_customuser'

    def get(self, request, pk):
        client = get_object_or_404(CustomUser, id=pk)

        data = {
            'id': client.id,
            'id_number': client.id_number,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'username': client.username,
            'email': client.email,
            'phone1': client.phone_number1,
            'phone2': client.phone_number2,
            'address': client.address,
        }
        return JsonResponse(data)


class CustomUserFormView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'inventory_management.add_customuser'

    def get(self, request, *args, **kwargs):
        form = CustomUserForm()
        user = request.user

        # Filtrar grupos según el rol del usuario
        if user.groups.filter(name='Administrators').exists():
            form.fields['groups'].queryset = Group.objects.all()
        elif user.groups.filter(name='Agents').exists():
            del form.fields['groups']
            # form.fields['groups'].queryset = Group.objects.filter(name='Clients')

        html = render_to_string('custom_user/partials/custom_user_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

    def post(self, request, *args, **kwargs):
        form = CustomUserForm(request.POST)

        if form.is_valid():
            # Verificar duplicados
            email = form.cleaned_data['email']
            id_number = form.cleaned_data['id_number']
            if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(
                    id_number=id_number).exists():
                return JsonResponse({'success': False, 'errors': {'email': 'Email or ID Number already exists.'}})

            if request.user.groups.filter(name='Agents').exists():
                form.save()
                user = CustomUser.objects.get(id_number=form.cleaned_data['id_number'])
                try:
                    group = Group.objects.get(name='Clients')
                    user.groups.add(group)
                except CustomUser.DoesNotExist:
                    return JsonResponse({'success': False, 'errors': {'User': 'This user does not exist.'}})
                except Group.DoesNotExist:
                    return JsonResponse({'success': False, 'errors': {'groups': 'This group does not exist.'}})
            elif request.user.groups.filter(name='Administrators').exists():
                form.save()

            return JsonResponse({'success': True})

        # Devolver errores si el formulario no es válido
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors})
