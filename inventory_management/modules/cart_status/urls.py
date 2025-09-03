from django.urls import path
from .views import (
    CartStatusListView,
    CartStatusDetailView,
    CartStatusCreateView,
    CartStatusUpdateView,
    CartStatusDeleteView,
)

urlpatterns = [
    path("", CartStatusListView.as_view(), name="cart_status_list"),
    path("create/", CartStatusCreateView.as_view(), name="cart_status_create"),
    # path("update/<str:pk>/", CartStatusUpdateView.as_view(), name="cart_status_update"),
    path("delete/<str:pk>/", CartStatusDeleteView.as_view(), name="cart_status_delete"),
]
