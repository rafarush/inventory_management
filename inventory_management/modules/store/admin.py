from django.contrib import admin
from inventory_management.modules.store.models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Store, StoreAdmin)
