from django.urls import path

from inventory_management.modules.wastage_record.views import WastageRecordListView, WastageRecordCreateView, \
    WastageRecordDeleteView, WastageRecordUpdateView

urlpatterns = [
    path('', WastageRecordListView.as_view(), name='wastage_record_list'),
    path('create/', WastageRecordCreateView.as_view(), name='wastage_record_create'),
    path('delete/<uuid:pk>/', WastageRecordDeleteView.as_view(), name='wastage_record_delete'),
    path('update/<uuid:pk>/', WastageRecordUpdateView.as_view(), name='wastage_record_update'),
]
