from django.contrib import admin

from inventory_management.modules.wastage_record.models import WastageRecord


class WastageRecordAdmin(admin.ModelAdmin):
    model = WastageRecord
    list_display = ('id', 'date', 'product', 'quantity', 'deleted')
    search_fields = ('id', 'date', 'product', 'quantity', 'deleted')
    ordering = ('date',)


admin.site.register(WastageRecord, WastageRecordAdmin)
