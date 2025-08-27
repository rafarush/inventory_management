from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventory_management.models import ProductCategory
from django.db.models.functions import Lower


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def clean_category(self):
        category = self.cleaned_data['category']
        formated_name = category.lower().replace(' ', '')
        all_products_names = [name.replace(' ', '').lower() for name in
                              ProductCategory.objects.values_list('category', flat=True)]
        if formated_name in all_products_names:
            raise ValidationError('This product already exists')
        return category
