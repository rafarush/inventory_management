from django.contrib import admin
from inventory_management.modules.daily_part_cart.models import DailyPartCart


class DailyPartCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')


admin.site.register(DailyPartCart, DailyPartCartAdmin)
