from django.urls import path, include
from inventory_management.views import Home, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('products/', include('inventory_management.modules.product.urls')),
    path('product_categories/', include('inventory_management.modules.product_category.urls')),
    path('accounts/', include('inventory_management.modules.custom_user.urls')),
]



