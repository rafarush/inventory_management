from django.contrib import admin
from inventory_management.modules.cart_status.models import CartStatus


class CartStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


admin.site.register(CartStatus, CartStatusAdmin)
