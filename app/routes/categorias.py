from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.services.categoria_service import (
    obtener_categorias,
    insertar_categoria,
    actualizar_categoria,
    desactivar_categoria,
    obtener_categoria_por_id,
    activar_categoria,
    obtener_categoria_por_nombre
)

categorias_bp = Blueprint(
    'categorias',
    __name__,
    url_prefix='/categorias'
)


# Función para validar el nombre de la categoría
def validar_categoria(nombre_categoria):

    nombre_categoria = nombre_categoria.strip()

    if len(nombre_categoria) == 0:

        return "El nombre de la categoría es obligatorio"

    if len(nombre_categoria) > 50:

        return "La categoría no puede exceder 50 caracteres"

    return None


# Ruta para listar todas las categorías
@categorias_bp.route('/')
def listar_categorias():

    categorias = obtener_categorias()

    return render_template(
        'categorias/listar.html',
        categorias=categorias
    )

# Ruta para crear una nueva categoría
@categorias_bp.route('/crear', methods=['POST'])
def crear_categoria():

    nombre_categoria = request.form.get(
        'nombre_categoria'
    )

    error = validar_categoria(
        nombre_categoria
    )

    if error:

        flash(
            error,
            'danger'
        )

        return redirect(
            url_for(
                'categorias.listar_categorias'
            )
        )

    categoria_existente = (
        obtener_categoria_por_nombre(
            nombre_categoria
        )
    )

    if categoria_existente:

        flash(
            'Ya existe una categoría con ese nombre',
            'danger'
        )

        return redirect(
            url_for(
                'categorias.listar_categorias'
            )
        )

    insertar_categoria(
        nombre_categoria
    )

    flash(
        f'Categoría "{nombre_categoria}" creada correctamente',
        'success'
    )

    return redirect(
        url_for(
            'categorias.listar_categorias'
        )
    )


# Ruta para editar una categoría existente
@categorias_bp.route('/editar/<int:id_categoria>',
                     methods=['POST'])
def editar_categoria(id_categoria):

    nombre_categoria = request.form.get(
        'nombre_categoria'
    )

    error = validar_categoria(
        nombre_categoria
    )

    if error:

        flash(
            error,
            'danger'
        )

        return redirect(
            url_for(
                'categorias.listar_categorias'
            )
        )

    categoria_existente = (
        obtener_categoria_por_nombre(
            nombre_categoria
        )
    )

    if (
        categoria_existente
        and
        categoria_existente['id_categoria'] != id_categoria
    ):

        flash(
            'Ya existe una categoría con ese nombre',
            'danger'
        )

        return redirect(
            url_for(
                'categorias.listar_categorias'
            )
        )

    actualizar_categoria(
        id_categoria,
        nombre_categoria
    )

    flash(
        f'Categoría "{nombre_categoria}" actualizada correctamente',
        'success'
    )

    return redirect(
        url_for(
            'categorias.listar_categorias'
        )
    )


# Ruta para eliminar (desactivar) una categoría
@categorias_bp.route('/desactivar/<int:id_categoria>')
def eliminar_categoria(id_categoria):

    categoria = obtener_categoria_por_id(
        id_categoria
    )

    desactivar_categoria(
        id_categoria
    )

    flash(
        f'Categoría "{categoria["nombre_categoria"]}" desactivada correctamente',
        'warning'
    )

    return redirect(
        url_for(
            'categorias.listar_categorias'
        )
    )


# Ruta para activar una categoría
@categorias_bp.route('/activar/<int:id_categoria>')
def activar_categoria_route(id_categoria):

    categoria = obtener_categoria_por_id(
        id_categoria
    )

    activar_categoria(
        id_categoria
    )

    flash(
        f'Categoría "{categoria["nombre_categoria"]}" activada correctamente',
        'success'
    )

    return redirect(
        url_for(
            'categorias.listar_categorias'
        )
    )