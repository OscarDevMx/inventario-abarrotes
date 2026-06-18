import re

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for
)
from app.services.producto_service import (
    obtener_productos,
    obtener_categorias,
    obtener_proveedores,
    insertar_producto,
    obtener_producto_por_id,
    obtener_producto_por_codigo,
    actualizar_producto,
    eliminar_producto,
    obtener_resumen_productos,
    activar_producto
)


productos_bp = Blueprint(
    'productos',
    __name__,
    url_prefix='/productos'
)

def validar_producto(data):

    codigo = data['codigo_barras'].strip()
    nombre = data['nombre'].strip()

    try:
        precio = float(data['precio'])
        stock_actual = int(data['stock_actual'])
        stock_minimo = int(data['stock_minimo'])

    except ValueError:

        return "Datos numéricos inválidos"

    # Código barras

    if not re.fullmatch(r'\d{1,12}', codigo):

        return "El código de barras debe contener únicamente números y máximo 12 dígitos"

    # Nombre

    if len(nombre) == 0:

        return "El nombre es obligatorio"

    if len(nombre) > 50:

        return "El nombre no puede exceder 50 caracteres"

    # Precio

    if precio <= 0 or precio > 999:

        return "El precio debe estar entre 0.01 y 999.00"

    # Stock

    if stock_actual < 0 or stock_actual > 9999:

        return "El stock actual debe estar entre 0 y 9999"

    # Stock mínimo

    if stock_minimo < 0 or stock_minimo > 9999:

        return "El stock mínimo debe estar entre 0 y 9999"

    return None



# Ruta para listar los productos
@productos_bp.route('/')
def listar_productos():

    busqueda = request.args.get(
        'busqueda',
        ''
    )

    categoria = request.args.get(
        'categoria',
        ''
    )

    estado = request.args.get(
        'estado',
        ''
    )

    productos = obtener_productos(
        busqueda,
        categoria,
        estado
    )
    


    categorias = obtener_categorias()

    resumen = obtener_resumen_productos()

    return render_template(
        'productos/listar.html',
        productos=productos,
        categorias=categorias,
        busqueda=busqueda,
        categoria=categoria,
        estado=estado,
        resumen=resumen
    )


# Ruta para mostrar el formulario de creación de producto
@productos_bp.route('/crear')
def crear_producto():

    categorias = obtener_categorias()
    proveedores = obtener_proveedores()

    return render_template(
        'productos/crear.html',
        categorias=categorias,
        proveedores=proveedores
    )

# Ruta para guardar el nuevo producto
@productos_bp.route('/guardar', methods=['POST'])
def guardar_producto():

    data = {
        'codigo_barras': request.form['codigo_barras'],
        'nombre': request.form['nombre'],
        'descripcion': request.form['descripcion'],
        'precio': request.form['precio'],
        'stock_actual': request.form['stock_actual'],
        'stock_minimo': request.form['stock_minimo'],
        'id_categoria': request.form['id_categoria'],
        'id_proveedor': request.form['id_proveedor']
    }

    error = validar_producto(data)

    if error:

        flash(error, 'danger')

        return redirect(
            url_for('productos.crear_producto')
        )
    
    producto_existente = obtener_producto_por_codigo(
        data['codigo_barras']
    )

    if producto_existente:

        flash(f'No se pudo dar de alta. Ya existe un producto con ese código de barras: "{data['codigo_barras']}"', 'danger')

        return redirect(
            url_for('productos.crear_producto')
        )

    insertar_producto(data)
    flash(f'Producto "{data["nombre"]}" creado correctamente','success')
    
    return redirect('/productos/')

# Ruta para mostrar el formulario de edición de producto
@productos_bp.route('/editar/<int:id_producto>')
def editar_producto(id_producto):

    producto = obtener_producto_por_id(id_producto)
    categorias = obtener_categorias()
    proveedores = obtener_proveedores()

    return render_template(
        'productos/editar.html',
        producto=producto,
        categorias=categorias,
        proveedores=proveedores
    )

# Ruta para actualizar el producto
@productos_bp.route('/actualizar/<int:id_producto>', methods=['POST'])
def actualizar_producto_route(id_producto):

    data = {
        'codigo_barras': request.form['codigo_barras'],
        'nombre': request.form['nombre'],
        'descripcion': request.form['descripcion'],
        'precio': request.form['precio'],
        'stock_actual': request.form['stock_actual'],
        'stock_minimo': request.form['stock_minimo'],
        'id_categoria': request.form['id_categoria'],
        'id_proveedor': request.form['id_proveedor']
    }

    error = validar_producto(data)

    if error:

        flash(error, 'danger')

        return redirect(
            url_for(
                'productos.editar_producto',
                id_producto=id_producto
            )
        )
    
    producto_existente = obtener_producto_por_codigo(
        data['codigo_barras']
    )

    if (
        producto_existente
        and
        producto_existente['id_producto'] != id_producto
    ):

        flash(f'No se pudo actualizar. Ya existe un producto con ese código de barras: "{data['codigo_barras']}"', 'danger')

        return redirect(
            url_for(
                'productos.editar_producto',
                id_producto=id_producto
            )
        )

    actualizar_producto(id_producto, data)
    flash(f'Producto "{data["nombre"]}" actualizado correctamente', 'primary')
    return redirect('/productos/')

# Ruta para eliminar un producto
@productos_bp.route('/eliminar/<int:id_producto>')
def eliminar_producto_route(id_producto):

    eliminar_producto(id_producto)
    flash(f'Producto "{obtener_producto_por_id(id_producto)["nombre"]}" eliminado exitosamente', 'danger')

    return redirect('/productos/')



@productos_bp.route(
    '/activar/<int:id_producto>'
)
def activar_producto_route(
    id_producto
):

    producto = obtener_producto_por_id(
        id_producto
    )

    activar_producto(
        id_producto
    )

    flash(
        f'Producto "{producto["nombre"]}" activado correctamente',
        'success'
    )

    return redirect(
        url_for(
            'productos.listar_productos'
        )
    )
