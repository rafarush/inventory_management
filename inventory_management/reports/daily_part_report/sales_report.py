# views/reports/daily_part.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.http import HttpResponse
import pandas as pd
from datetime import datetime, timedelta

from inventory_management.modules.daily_part.models import DailyPart
from inventory_management.reports.base_report import BaseReportView


class SalesReportView(BaseReportView):
    """
    Vista para generar reportes de ventas (utilidad neta, inversión, retornos).
    Permite visualizar en HTML, exportar a Excel o PDF, y muestra gráficos.
    """
    template_name = 'reports/daily_part_report/sales_report.html'
    permission_required = 'inventory_management.view_product'

    def get(self, request, *args, **kwargs):
        # --- 1. Rango de fechas ---
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            end_dt = datetime.today().date()
            start_dt = end_dt - timedelta(days=6)  # últimos 7 días
            start_date = start_dt.strftime("%Y-%m-%d")
            end_date = end_dt.strftime("%Y-%m-%d")
        else:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Validación: máximo 30 días
        if (end_dt - start_dt).days > 30:
            return HttpResponse(_("The maximum allowed range is 30 days."), status=400)

        # --- 2. Queryset filtrado ---
        daily_parts = DailyPart.objects.filter(date__range=[start_date, end_date])

        # --- 3. Transformar a DataFrame ---
        data = [
            {
                "date": dp.date,
                "net_profit": float(dp.net_profit or 0),
                "money_invested": float(dp.money_invested or 0),
                "money_return_total": float(dp.money_return_total or 0),
            }
            for dp in daily_parts
        ]

        df = pd.DataFrame(data)

        if df.empty:
            df = pd.DataFrame(columns=["date", "net_profit", "money_invested", "money_return_total"])
        else:
            # 🔹 Conversión de fecha → string para Altair
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            df = df.sort_values(by="date")

        # --- 4. Gráfico (función: línea + puntos) ---
        chart = None
        if not df.empty:
            chart = self.generate_function_chart(
                df,
                x_col="date",
                y_col="net_profit",
                title=_("Daily Net Profit Function"),
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
            return self.generate_excel(df, filename="daily_profit.xlsx")

        if export_format == "pdf":
            return self.generate_pdf(
                template_name="reports/daily_part_report/sales_report_pdf.html",
                context=context,
                filename="daily_profit.pdf",
            )

        # --- 7. Render HTML ---
        return render(request, self.template_name, context)
