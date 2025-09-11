from django.contrib import admin
from inventory_management.modules.daily_part.models import DailyPart


class DailyPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')


admin.site.register(DailyPart, DailyPartAdmin)
