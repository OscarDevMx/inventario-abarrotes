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
    obtener_proveedor_por_id,
    obtener_proveedor_por_nombre
)

proveedores_bp = Blueprint(
    'proveedores',
    __name__,
    url_prefix='/proveedores'
)

# Validación de datos de proveedor
def validar_proveedor(data):

    nombre = data['nombre'].strip()

    telefono = data['telefono'].strip()

    if len(nombre) == 0:

        return 'El nombre es obligatorio'

    if len(nombre) > 50:

        return 'El nombre no puede exceder 50 caracteres'

    if telefono:

        if not telefono.isdigit():

            return 'El teléfono solo puede contener números'

        if len(telefono) > 10:

            return 'El teléfono no puede exceder 10 dígitos'

    return None


# Rutas para proveedores
@proveedores_bp.route('/')
def listar_proveedores():

    proveedores = obtener_proveedores()

    return render_template(
        'proveedores/listar.html',
        proveedores=proveedores
    )


# Rutas para crear proveedores
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

    error = validar_proveedor(
        data
    )

    if error:

        flash(
            error,
            'danger'
        )

        return redirect(
            url_for(
                'proveedores.listar_proveedores'
            )
        )
    
    proveedor_existente = (
        obtener_proveedor_por_nombre(
            data['nombre']
        )
    )

    if proveedor_existente:

        flash(f'No se pudo crear. Ya existe un proveedor con ese nombre: "{data["nombre"]}"', 'danger')   

        return redirect(
            url_for(
                'proveedores.listar_proveedores'
            )
        )

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


# Rutas para editar proveedores
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

    error = validar_proveedor(
        data
    )

    if error:

        flash(
            error,
            'danger'
        )

        return redirect(
            url_for(
                'proveedores.listar_proveedores'
            )
        )

    proveedor_existente = (
        obtener_proveedor_por_nombre(
            data['nombre']
        )
    )

    if (
        proveedor_existente
        and
        proveedor_existente['id_proveedor'] != id_proveedor
    ):

        flash(f'No se pudo actualizar. Ya existe un proveedor con ese nombre: "{data["nombre"]}"', 'danger')

        return redirect(
            url_for(
                'proveedores.listar_proveedores'
            )
        )
    
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


# Rutas para desactivar proveedores
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


# Rutas para activar proveedores
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



