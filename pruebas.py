from app.database.connection import get_connection


def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            p.id_producto,
            p.codigo_barras,
            p.nombre,
            c.nombre_categoria,
            pr.nombre AS proveedor,
            p.precio,
            p.stock_actual
        FROM productos p
        JOIN categorias c
            ON p.id_categoria = c.id_categoria
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        WHERE p.activo = TRUE
        ORDER BY p.nombre
    """

    cursor.execute(query)
    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return productos

def obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_categoria, nombre_categoria
        FROM categorias
        WHERE activo = TRUE
        ORDER BY nombre_categoria
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def obtener_proveedores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        WHERE activo = TRUE
        ORDER BY nombre
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def insertar_producto(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO productos
        (
            codigo_barras,
            nombre,
            descripcion,
            precio,
            stock_actual,
            stock_minimo,
            id_categoria,
            id_proveedor,
            id_usuario
        )
        VALUES
        (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s
        )
    """

    valores = (
        data['codigo_barras'],
        data['nombre'],
        data['descripcion'],
        data['precio'],
        data['stock_actual'],
        data['stock_minimo'],
        data['id_categoria'],
        data['id_proveedor'],
        1
    )

    cursor.execute(query, valores)

    conn.commit()

    cursor.close()
    conn.close()

# Función para obtener un producto por su ID
def obtener_producto_por_id(id_producto):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM productos
        WHERE id_producto = %s
    """

    cursor.execute(query, (id_producto,))
    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    return producto

# Función para actualizar un producto existente
def actualizar_producto(id_producto, data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE productos
        SET
            codigo_barras=%s,
            nombre=%s,
            descripcion=%s,
            precio=%s,
            stock_actual=%s,
            stock_minimo=%s,
            id_categoria=%s,
            id_proveedor=%s
        WHERE id_producto=%s
    """

    valores = (
        data['codigo_barras'],
        data['nombre'],
        data['descripcion'],
        data['precio'],
        data['stock_actual'],
        data['stock_minimo'],
        data['id_categoria'],
        data['id_proveedor'],
        id_producto
    )

    cursor.execute(query, valores)

    conn.commit()

    cursor.close()
    conn.close()

# Función para eliminar un producto (marcar como inactivo)
def eliminar_producto(id_producto):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE productos
        SET activo = FALSE
        WHERE id_producto = %s
    """

    cursor.execute(query, (id_producto,))
    conn.commit()

    cursor.close()
    conn.close()