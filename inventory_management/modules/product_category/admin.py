from django.contrib import admin

from inventory_management.models import ProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)


admin.site.register(ProductCategory, ProductCategoryAdmin)
