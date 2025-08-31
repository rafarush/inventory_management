from django.urls import path
from .views import (
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView
)

urlpatterns = [
    path('', WorkerListView.as_view(), name='worker_list'),
    path('detail/<str:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
    path('create/', WorkerCreateView.as_view(), name='worker_create'),
    path('update/<str:pk>/', WorkerUpdateView.as_view(), name='worker_update'),
    path('delete/<str:pk>/', WorkerDeleteView.as_view(), name='worker_delete'),
]
