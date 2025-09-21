# views/reports/charge_cart.py
from django.views import View
from django.shortcuts import render
from inventory_management.modules.charge_cart.models import ChargeCart
from inventory_management.reports.base_report import BaseReportView
import pandas as pd


class TopProductsReportView(BaseReportView):
    template_name = 'reports/product_report/top_products_report.html'

    def get(self, request, *args, **kwargs):
        # --- 1. Filtro por rango de fechas ---
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        charge_carts = ChargeCart.objects.all()
        if start_date and end_date:
            charge_carts = charge_carts.filter(created_at__date__range=[start_date, end_date])

        # --- 2. Calcular cantidad vendida ---
        data = []
        for cc in charge_carts:
            sold = (cc.amount_sent or 0) - (cc.amount_received or 0)
            data.append({
                'product_id': cc.product.id,
                'product_name': getattr(cc.product, 'name', str(cc.product.id)),
                'sold': sold
            })

        df = pd.DataFrame(data)

        # --- 3. Validar DataFrame ---
        if df.empty:
            df = pd.DataFrame(columns=['product_id', 'product_name', 'sold'])
        else:
            df['sold'] = pd.to_numeric(df['sold'], errors='coerce').fillna(0)

        # --- 4. Agrupar por producto ---
        df_grouped = df.groupby(['product_id', 'product_name'], as_index=False)['sold'].sum()
        df_grouped = df_grouped.sort_values(by='sold', ascending=False)

        # --- 5. Generar gráfico ---
        chart = None
        if not df_grouped.empty:
            chart = self.generate_chart(
                df_grouped,
                x_col='product_name',
                y_col='sold',
                title='Productos más vendidos'
            )

        context = {
            'df': df_grouped.to_dict('records'),
            'chart': chart,
        }

        # --- 6. Exportar Excel ---
        if request.GET.get('format') == 'excel':
            return self.generate_excel(df_grouped, filename='top_products.xlsx')

        # --- 7. Exportar PDF ---
        if request.GET.get('format') == 'pdf':
            # Aquí llamas manualmente al template específico para PDF
            return self.generate_pdf(
                template_name='reports/product_report/top_products_report_pdf.html',
                context=context,
                filename='top_products.pdf'
            )

        # --- 8. Render HTML ---
        return render(request, self.template_name, context)
