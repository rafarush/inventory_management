from django.views import View
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import plotly.express as px
import altair as alt
import pandas as pd
import io
import base64
from django.utils.translation import gettext as _



class BaseReportView(View):
    """
    Clase base para reportes.
    Contiene métodos reutilizables para:
    - Exportar PDF usando un template específico para PDF
    - Exportar Excel
    - Generar gráficos
    """

    import plotly.express as px
    import io
    import base64

    def generate_chart(self, df, x_col, y_col, rolling_window=3, title=''):
        """
        Genera un gráfico de barras con media móvil usando Altair y devuelve base64 para PDF/HTML.
        """
        # --- Calcular media móvil ---
        df['rolling_mean'] = df[y_col].rolling(window=rolling_window, min_periods=1).mean()

        # --- Crear gráfico Altair ---
        bar = alt.Chart(df).mark_bar(color='#4C78A8').encode(
            x=alt.X(x_col, sort=None, axis=alt.Axis(title=" ")),
            y=y_col,
            tooltip=[x_col, y_col, 'rolling_mean']
        )

        line = alt.Chart(df).mark_line(color='orange', strokeWidth=3).encode(
            x=alt.X(x_col, sort=None),
            y='rolling_mean'
        )

        chart = (bar + line).properties(
            title=" ",
            width=600,
            height=400
        ).interactive()

        # --- Exportar a PNG ---
        buf = io.BytesIO()
        chart.save(buf, format='png')
        buf.seek(0)
        chart_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return chart_base64

    def generate_excel(self, df, filename=None):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)

        # Si no se pasa filename, usamos traducción
        if not filename:
            filename = _("report") + ".xlsx"

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def generate_pdf(self, template_name, context, filename='report.pdf', pdf_template_suffix='_pdf'):
        parts = template_name.rsplit('.', 1)  # separar extensión
        pdf_template_name = f"{parts[0]}{pdf_template_suffix}.{parts[1]}"

        try:
            html_string = render_to_string(pdf_template_name, context)
        except Exception:
            html_string = render_to_string(template_name, context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        pisa_status = pisa.CreatePDF(
            io.StringIO(html_string),
            dest=response,
            encoding='UTF-8'
        )

        if pisa_status.err:
            return HttpResponse(_("Error generating PDF"), status=500)
        return response

    def generate_function_chart(self, df, x_col, y_col, title=''):
        """
        Genera un gráfico de línea (tipo función) con Altair y devuelve base64 para PDF/HTML.
        """
        # Asegurar que las fechas o x sean strings o datetime
        if pd.api.types.is_datetime64_any_dtype(df[x_col]):
            df[x_col] = df[x_col].astype(str)

        # --- Crear gráfico tipo función (línea continua) ---
        line = alt.Chart(df).mark_line(color='#1f77b4', strokeWidth=3).encode(
            x=alt.X(x_col, sort=None, axis=alt.Axis(title=None)),  # 👈 sin título
            y=alt.Y(y_col, axis=alt.Axis(title=None)),  # 👈 sin título
            tooltip=[x_col, y_col]
        )

        points = alt.Chart(df).mark_circle(size=60, color='orange').encode(
            x=x_col,
            y=y_col,
            tooltip=[x_col, y_col]
        )

        chart = (line + points).properties(
            title=title or f"{y_col} over {x_col}",
            width=600,
            height=400
        ).interactive()

        # --- Exportar a PNG (base64) ---
        buf = io.BytesIO()
        chart.save(buf, format='png')
        buf.seek(0)
        chart_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return chart_base64
