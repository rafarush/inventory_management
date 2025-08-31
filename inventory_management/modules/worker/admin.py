from django.contrib import admin
from inventory_management.modules.worker.models import Worker


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary', 'phone')


admin.site.register(Worker, WorkerAdmin)
