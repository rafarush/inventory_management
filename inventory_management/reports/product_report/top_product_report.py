# views/reports/charge_cart.py
from django.views import View
from django.shortcuts import render
from inventory_management.modules.charge_cart.models import ChargeCart
from inventory_management.reports.base_report import BaseReportView
import pandas as pd
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class TopProductsReportView(BaseReportView, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = 'reports/product_report/top_products_report.html'
    permission_required = 'inventory_management.view_product'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, 'access_denied.html', status=403)
        return super().handle_no_permission()

    def get(self, request, *args, **kwargs):
        # --- 1. Filtro por rango de fechas ---
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        charge_carts = ChargeCart.objects.all()
        if start_date and end_date:
            # 🔹 Se usa el campo date de DailyPartCart
            charge_carts = charge_carts.filter(daily_part_cart__date__range=[start_date, end_date])

        # --- 2. Calcular cantidad vendida ---
        data = []
        for cc in charge_carts:
            sold = (cc.amount_sent or 0) - (cc.amount_received or 0)
            data.append({
                'product': cc.product.id,
                'name': getattr(cc.product, 'name', str(cc.product.id)),
                'sold': sold
            })

        # --- 3. Crear DataFrame ---
        df = pd.DataFrame(data)
        if df.empty:
            df = pd.DataFrame(columns=['product', 'name', 'sold'])
        else:
            df['sold'] = pd.to_numeric(df['sold'], errors='coerce').fillna(0)

        # --- 4. Agrupar por producto ---
        df_grouped = df.groupby(['product', 'name'], as_index=False)['sold'].sum()
        df_grouped = df_grouped.sort_values(by='sold', ascending=False)

        # --- 5. Generar gráfico ---
        chart = None
        if not df_grouped.empty:
            chart = self.generate_chart(
                df_grouped,
                x_col='name',
                y_col='sold',
                title=_("Best-selling products")
            )

        # --- 6. Contexto ---
        context = {
            'df': df_grouped.to_dict('records'),
            'chart': chart,
        }

        # --- 7. Exportar Excel ---
        if request.GET.get('format') == 'excel':
            return self.generate_excel(df_grouped, filename='top_products.xlsx')

        # --- 8. Exportar PDF ---
        if request.GET.get('format') == 'pdf':
            return self.generate_pdf(
                template_name='reports/product_report/top_products_report_pdf.html',
                context=context,
                filename='top_products.pdf'
            )

        # --- 9. Render HTML ---
        return render(request, self.template_name, context)
