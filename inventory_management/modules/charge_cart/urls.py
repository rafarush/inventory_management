# inventory_management/modules/charge_cart/urls.py
from django.urls import path
from .views import (
    ChargeCartListView, ChargeCartCreateView, ChargeCartDetailView,
    ChargeCartDeleteView, ChargeCartUpdateView, ChargeCartFinishView
)

urlpatterns = [
    path('', ChargeCartListView.as_view(), name='charge_cart_list'),
    path('create/', ChargeCartCreateView.as_view(), name='charge_cart_create'),
    path('<uuid:pk>/', ChargeCartDetailView.as_view(), name='charge_cart_detail'),
    path('update/<uuid:pk>/', ChargeCartUpdateView.as_view(), name='charge_cart_update'),
    path('delete/<uuid:pk>/', ChargeCartDeleteView.as_view(), name='charge_cart_delete'),
    path('finish/<str:pk>', ChargeCartFinishView.as_view(), name='charge_cart_finish'),
]
