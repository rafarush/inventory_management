from django.urls import path, include
from inventory_management.views import Home

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('auth/', include('inventory_management.modules.auth.urls'), name='auth'),
    path('products/', include('inventory_management.modules.product.urls')),
    path('cart/', include('inventory_management.modules.cart.urls')),
    path('product_categories/', include('inventory_management.modules.product_category.urls')),
    path('users/', include('inventory_management.modules.custom_user.urls')),
    path('confirm-email/', include('inventory_management.modules.email_services.urls')),
    path('workers/', include('inventory_management.modules.worker.urls')),
    path('account/', include('inventory_management.modules.email_services.urls')),
]



