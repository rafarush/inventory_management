from django.urls import path
from .views import ProductCategoryListView, ProductCategoryCreateView, ProductCategoryUpdateView, \
    ProductCategoryDeleteView

urlpatterns = [
    path('', ProductCategoryListView.as_view(), name='product_category_list'),
    path('create/', ProductCategoryCreateView.as_view(), name='product_category_create'),
    path('update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='product_category_update'),
    path('delete/<int:pk>/', ProductCategoryDeleteView.as_view(), name='product_category_delete'),
]