from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<uuid:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('detail/<uuid:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('delete/<str:pk>', ProductDeleteView.as_view(), name='product_delete'),
]
