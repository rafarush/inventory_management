from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.models import Permission, Group
from inventory_management.modules.custom_user.forms import CustomUserForm, CustomUserChangeForm
from inventory_management.models import CustomUser
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


class CustomUserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'custom_user/custom_user_list.html'
    permission_required = 'inventory_management.view_customuser'

    def get_queryset(self):
        # Retorna solo los usuarios que no están eliminados soft
        qs = super().get_queryset()
        return qs.filter(deleted=None)

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

    # def form_valid(self, form):
    #     print("llego a guardar el form")
    #     user = form.save(commit=False)
    #     user.is_confirmed = False
    #     user.save()
    #
    #     token = default_token_generator.make_token(user)
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     print("uid user antes")
    #     print(uid)
    #     print("token user antes")
    #     print(token)
    #     current_site = get_current_site(self.request)
    #     mail_subject = 'Confirma tu correo'
    #     context = {
    #         'user': user,
    #         'domain': current_site.domain,
    #         'uid': uid,
    #         'token': token,
    #     }
    #     print("antes del email")
    #     user.send_email(mail_subject, 'emails/email_confirmation_template.html', context)
    #     print("despues del email")

        return super().form_valid(form)

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

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        form = CustomUserChangeForm(instance=user)
        html = render_to_string('custom_user/partials/custom_user_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors})

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
        html = render_to_string('custom_user/partials/custom_user_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

    def post(self, request, *args, **kwargs):
        form = CustomUserForm(request.POST)

        if form.is_valid():
            # Verificar duplicados
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'errors': {'email': 'Email already exists.'}})

            # form.save()
            user = form.save(commit=False)
            user.is_confirmed = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid user antes")
            print(uid)
            print("token user antes")
            print(token)
            current_site = get_current_site(self.request)
            mail_subject = 'Confirma tu correo'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            }
            print("antes del email")
            user.send_email(mail_subject, 'emails/email_confirmation_template.html', context)
            print("despues del email")

            return JsonResponse({'success': True})

        # Devolver errores si el formulario no es válido
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors})
