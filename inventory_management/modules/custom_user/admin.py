from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from inventory_management.modules.custom_user.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)


