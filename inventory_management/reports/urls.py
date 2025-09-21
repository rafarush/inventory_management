# inventory_management/modules/reports/urls.py
from django.urls import path
from .product_report.top_product_report import TopProductsReportView
from .daily_part_report.sales_report import SalesReportView
from .worker_report.best_worker_report import BestWorkerReportView

app_name = "reports"

urlpatterns = [
    path("top-products/", TopProductsReportView.as_view(), name="top_products"),
    path("sales-report/", SalesReportView.as_view(), name="sales_report"),
    path("worker-report/", BestWorkerReportView.as_view(), name="worker_report"),
]
