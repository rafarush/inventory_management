from django.contrib import admin
from inventory_management.modules.product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'price')


admin.site.register(Product, ProductAdmin)
