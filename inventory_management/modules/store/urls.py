from django.urls import path
from .views import StoreDetailView, StoreUpdateView

urlpatterns = [
    path("", StoreDetailView.as_view(), name="store_detail"),
    path("update/", StoreUpdateView.as_view(), name="store_update"),
]
