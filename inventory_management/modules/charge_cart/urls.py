# inventory_management/modules/charge_cart/urls.py
from django.urls import path
from .views import (
    ChargeCartListView,
    ChargeCartCreateView,
    ChargeCartDetailView,
    ChargeCartUpdateView,
    ChargeCartDeleteView, ChargeCartFinishView
)

urlpatterns = [
    # 🔹 LISTADOS
    path('', ChargeCartListView.as_view(), name='charge_cart_list'),  # listado general
    path('daily/<uuid:daily_part_cart_id>/', ChargeCartListView.as_view(), name='charge_cart_list_by_daily'),  # filtrado por DailyPartCart

    # 🔹 CREAR
    path('create/', ChargeCartCreateView.as_view(), name='charge_cart_create'),
    path('create/<uuid:daily_part_cart_id>/', ChargeCartCreateView.as_view(), name='charge_cart_create_by_daily'),  # crear vinculado a DailyPartCart

    path('<uuid:pk>/', ChargeCartDetailView.as_view(), name='charge_cart_detail'),

    path('update/<uuid:pk>/', ChargeCartUpdateView.as_view(), name='charge_cart_update'),

    path('delete/<uuid:pk>/', ChargeCartDeleteView.as_view(), name='charge_cart_delete'),
    path('finish/<uuid:pk>/', ChargeCartFinishView.as_view(), name='charge_cart_finish'),

]
