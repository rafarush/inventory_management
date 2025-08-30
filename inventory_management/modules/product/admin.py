from django.contrib import admin
from inventory_management.modules.product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock',)


admin.site.register(Product, ProductAdmin)
