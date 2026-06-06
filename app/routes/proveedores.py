from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.services.proveedor_service import (
    obtener_proveedores,
    insertar_proveedor,
    actualizar_proveedor,
    desactivar_proveedor,
    activar_proveedor,
    obtener_proveedor_por_id
)

proveedores_bp = Blueprint(
    'proveedores',
    __name__,
    url_prefix='/proveedores'
)


@proveedores_bp.route('/')
def listar_proveedores():

    proveedores = obtener_proveedores()

    return render_template(
        'proveedores/listar.html',
        proveedores=proveedores
    )


@proveedores_bp.route(
    '/crear',
    methods=['POST']
)
def crear_proveedor():

    data = {

        'nombre':
        request.form['nombre'],

        'telefono':
        request.form['telefono'],

        'email':
        request.form['email']

    }

    insertar_proveedor(data)

    flash(
        f'Proveedor "{data["nombre"]}" creado correctamente',
        'success'
    )

    return redirect(
        url_for(
            'proveedores.listar_proveedores'
        )
    )



@proveedores_bp.route(
    '/editar/<int:id_proveedor>',
    methods=['POST']
)
def editar_proveedor(id_proveedor):

    data = {

        'nombre':
        request.form['nombre'],

        'telefono':
        request.form['telefono'],

        'email':
        request.form['email']

    }

    actualizar_proveedor(
        id_proveedor,
        data
    )

    flash(
        f'Proveedor "{data["nombre"]}" actualizado correctamente',
        'success'
    )

    return redirect(
        url_for(
            'proveedores.listar_proveedores'
        )
    )



@proveedores_bp.route(
    '/desactivar/<int:id_proveedor>'
)
def desactivar_proveedor_route(
    id_proveedor
):

    proveedor = obtener_proveedor_por_id(
        id_proveedor
    )

    desactivar_proveedor(
        id_proveedor
    )

    flash(
        f'Proveedor "{proveedor["nombre"]}" desactivado correctamente',
        'warning'
    )

    return redirect(
        url_for(
            'proveedores.listar_proveedores'
        )
    )


@proveedores_bp.route(
    '/activar/<int:id_proveedor>'
)
def activar_proveedor_route(
    id_proveedor
):

    proveedor = obtener_proveedor_por_id(
        id_proveedor
    )

    activar_proveedor(
        id_proveedor
    )

    flash(
        f'Proveedor "{proveedor["nombre"]}" activado correctamente',
        'success'
    )

    return redirect(
        url_for(
            'proveedores.listar_proveedores'
        )
    )



