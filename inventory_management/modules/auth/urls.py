from django.urls import path
from inventory_management.modules.auth.views import CustomLoginView, CustomLogoutView, SignUpView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]