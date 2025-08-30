from django.urls import path
from inventory_management.modules.email_services.views import  activate_email

urlpatterns = [
    path('confirm-email/<uidb64>/<token>/', activate_email, name='confirm_email'),
]