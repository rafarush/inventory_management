from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from inventory_management.modules.custom_user.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'get_groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'get_groups')
    ordering = ('username',)

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Groups'


admin.site.register(CustomUser, CustomUserAdmin)


