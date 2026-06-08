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
