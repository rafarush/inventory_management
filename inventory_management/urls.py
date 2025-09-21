from django.urls import path, include
from inventory_management.views import Home

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('auth/', include('inventory_management.modules.auth.urls')),
    path('products/', include('inventory_management.modules.product.urls')),
    path('cart/', include('inventory_management.modules.cart.urls')),
    path('reports/', include('inventory_management.reports.urls')),
    path('charge_cart/', include('inventory_management.modules.charge_cart.urls')),
    path('users/', include('inventory_management.modules.custom_user.urls')),
    path('confirm-email/', include('inventory_management.modules.email_services.urls')),
    path('workers/', include('inventory_management.modules.worker.urls')),
    path('daily_part_cart/', include('inventory_management.modules.daily_part_cart.urls')),
    path('daily_part/', include('inventory_management.modules.daily_part.urls')),
    path('store/', include('inventory_management.modules.store.urls')),
    path('account/', include('inventory_management.modules.email_services.urls')),
    path('wastage_records/', include('inventory_management.modules.wastage_record.urls'))
]



