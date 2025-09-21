# inventory_management/modules/reports/urls.py
from django.urls import path
from .product_report.top_product_report import TopProductsReportView

app_name = "reports"

urlpatterns = [
    path("top-products/", TopProductsReportView.as_view(), name="top_products"),
]
