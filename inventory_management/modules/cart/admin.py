from django.contrib import admin
from inventory_management.modules.cart.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(Cart, CartAdmin)
