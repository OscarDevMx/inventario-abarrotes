from flask import (
    Blueprint,
    render_template
)

from app.services.movimiento_service import (
    obtener_movimientos
)

movimientos_bp = Blueprint(

    'movimientos',
    __name__,

    url_prefix='/movimientos'

)


@movimientos_bp.route('/')
def listar_movimientos():

    movimientos = obtener_movimientos()

    return render_template(

        'movimientos/listar.html',

        movimientos=movimientos

    )