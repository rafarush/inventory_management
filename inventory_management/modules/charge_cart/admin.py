from django.contrib import admin
from inventory_management.modules.charge_cart.models import ChargeCart


class ChargeCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')


admin.site.register(ChargeCart, ChargeCartAdmin)
