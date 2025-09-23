# views/reports/worker_report.py
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.http import HttpResponse
import pandas as pd
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from inventory_management.modules.daily_part_cart.models import DailyPartCart
from inventory_management.reports.base_report import BaseReportView


class BestWorkerReportView(BaseReportView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Reporte de trabajadores que más han generado ganancias.
    Permite visualizar en HTML, exportar a Excel o PDF, y muestra gráficos.
    """
    template_name = "reports/worker_report/best_worker_report.html"
    permission_required = 'inventory_management.view_worker'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()

    def get(self, request, *args, **kwargs):
        # --- 1. Rango de fechas ---
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            # 🔹 Por defecto: últimos 30 días
            end_dt = datetime.today().date()
            start_dt = end_dt - timedelta(days=29)
            start_date = start_dt.strftime("%Y-%m-%d")
            end_date = end_dt.strftime("%Y-%m-%d")
        else:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

        # 🔹 Validación: máximo 365 días
        if (end_dt - start_dt).days > 365:
            return HttpResponse(_("The maximum allowed range is 1 year."), status=400)

        # --- 2. Queryset filtrado ---
        worker_parts = DailyPartCart.objects.filter(date__range=[start_date, end_date])

        # --- 3. Transformar a DataFrame ---
        data = [
            {
                "worker": dp.worker.name,
                "net_profit": float(dp.net_profit or 0),
                "revenue": float(dp.revenue or 0),
                "money_invested": float(dp.money_invested or 0),
                "date": dp.date,
            }
            for dp in worker_parts
        ]

        df = pd.DataFrame(data)

        if df.empty:
            df = pd.DataFrame(columns=["worker", "net_profit", "revenue", "money_invested", "date"])
        else:
            # 🔹 Agrupar por trabajador
            df = (
                df.groupby("worker", as_index=False)
                .agg({
                    "net_profit": "sum",
                    "revenue": "sum",
                    "money_invested": "sum",
                })
                .sort_values(by="net_profit", ascending=False)
            )

        # --- 4. Gráfico (barras de ganancias por trabajador) ---
        chart = None
        if not df.empty:
            chart = self.generate_function_chart(
                df,
                x_col="worker",
                y_col="net_profit",
                title=_("Workers Net Profit"),
            )

        # --- 5. Contexto ---
        context = {
            "df": df.to_dict("records"),
            "chart": chart,
            "start_date": start_date,
            "end_date": end_date,
        }

        # --- 6. Exportaciones ---
        export_format = request.GET.get("format")

        if export_format == "excel":
            return self.generate_excel(df, filename="workers_profit.xlsx")

        if export_format == "pdf":
            return self.generate_pdf(
                template_name="reports/worker_report/best_worker_report_pdf.html",
                context=context,
                filename="workers_profit.pdf",
            )

        # --- 7. Render HTML ---
        return render(request, self.template_name, context)
