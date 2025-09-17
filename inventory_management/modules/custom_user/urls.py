from django.urls import path
from inventory_management.modules.custom_user.views import (
    CustomUserList, CustomUserCreate, CustomUserDelete, CustomUserDetail,
    CustomUserUpdate, CustomUserClientsList, CustomUserDetailsJSON, CustomUserFormView
)

urlpatterns = [
    path('', CustomUserList.as_view(), name='custom_user_list'),
    path('create/', CustomUserCreate.as_view(), name='custom_user_create'),
    path('delete/<uuid:pk>/', CustomUserDelete.as_view(), name='custom_user_delete'),
    path('detail/<uuid:pk>', CustomUserDetail.as_view(), name='custom_user_detail'),
    path('update/<uuid:pk>/', CustomUserUpdate.as_view(), name='custom_user_update'),
    path('clients/', CustomUserClientsList.as_view(), name='custom_user_get_clients'),
    path('client/<uuid:pk>/', CustomUserDetailsJSON.as_view(), name='custom_user_get_json'),
    path('form/', CustomUserFormView.as_view(), name='custom_user_form'),  # Nueva ruta
]