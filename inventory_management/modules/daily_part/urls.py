from django.urls import path

from inventory_management.modules.daily_part.views import DailyPartCreateView, DailyPartListView, DailyPartDetailView, \
    DailyPartFinishView

urlpatterns = [
    path('', DailyPartListView.as_view(), name='daily_part_list'),
    path('create/', DailyPartCreateView.as_view(), name='daily_part_create'),
    path('<uuid:pk>/', DailyPartDetailView.as_view(), name='daily_part_detail'),
    path('finish/<uuid:pk>/', DailyPartFinishView.as_view(), name='daily_part_finish'),
]
