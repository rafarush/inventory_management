from django.urls import path
from .views import (
    CartListView,
    CartDetailView,
    CartCreateView,
    CartUpdateView,
    CartDeleteView,
)

urlpatterns = [
    path("", CartListView.as_view(), name="cart_list"),
    #path("create/", CartCreateView.as_view(), name="cart_create"),
    # path("update/<str:pk>/", CartUpdateView.as_view(), name="cart_update"),
    path("delete/<str:pk>/", CartDeleteView.as_view(), name="cart_delete"),
]
