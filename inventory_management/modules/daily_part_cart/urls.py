from django.urls import path
from inventory_management.modules.daily_part_cart.views import (
    DailyPartCartListView, DailyPartCartCreateView, DailyPartCartDetailView,
    DailyPartCartUpdateView, DailyPartCartDeleteView
)

urlpatterns = [
    path('', DailyPartCartListView.as_view(), name='daily_part_cart_list'),
    path('create/', DailyPartCartCreateView.as_view(), name='daily_part_cart_create'),
    path('<uuid:pk>/', DailyPartCartDetailView.as_view(), name='daily_part_cart_detail'),
    path('update/<uuid:pk>/', DailyPartCartUpdateView.as_view(), name='daily_part_cart_update'),
    path('delete/<uuid:pk>/', DailyPartCartDeleteView.as_view(), name='daily_part_cart_delete'),
]
