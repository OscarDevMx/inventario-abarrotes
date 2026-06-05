from flask import (
    Blueprint,
    render_template
)

from app.services.reporte_service import (

    obtener_kpis_dashboard,
    obtener_ultimas_ventas,
    obtener_top_productos

)

reportes_bp = Blueprint(

    'reportes',
    __name__,

    url_prefix='/reportes'

)


@reportes_bp.route('/')
def dashboard_reportes():

    kpis = obtener_kpis_dashboard()

    ventas = obtener_ultimas_ventas()

    top = obtener_top_productos()

    return render_template(

        'reportes/dashboard.html',

        kpis=kpis,
        ventas=ventas,
        top=top

    )