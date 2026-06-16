from app.database.connection import get_connection


def obtener_productos(busqueda='', categoria='', estado=''):

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
            p.stock_actual,
            p.stock_minimo,
            p.activo
        FROM productos p
        JOIN categorias c
            ON p.id_categoria = c.id_categoria
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        WHERE 1=1
    """

    valores = []

    if categoria:

        query += """
            AND p.id_categoria = %s
        """

        valores.append(
            categoria
        )

    if estado == 'activo':

        query += """
            AND p.activo = TRUE
        """

    elif estado == 'inactivo':

        query += """
            AND p.activo = FALSE
        """

    if busqueda:

        query += """
            AND (
                p.nombre LIKE %s
                OR p.codigo_barras LIKE %s
            )
        """

        termino = f"%{busqueda}%"

        valores.extend([
            termino,
            termino
        ])

    query += """
        ORDER BY p.nombre
    """

    cursor.execute(
        query,
        valores
    )

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

# Función para insertar un nuevo producto
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
    id_producto = cursor.lastrowid

    query_movimiento = """
        INSERT INTO movimientos_inventario
        (
            id_producto,
            id_usuario,
            tipo_movimiento,
            cantidad,
            motivo
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    valores_movimiento = (
        id_producto,
        1,
        'ENTRADA',
        data['stock_actual'],
        'Alta de producto'
    )

    cursor.execute(
        query_movimiento,
        valores_movimiento
    )

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

def obtener_producto_por_codigo(codigo_barras):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id_producto
        FROM productos
        WHERE codigo_barras = %s
    """

    cursor.execute(
        query,
        (codigo_barras,)
    )

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


    cursor.execute(
        """
        SELECT stock_actual
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto_actual = cursor.fetchone()

    stock_anterior = producto_actual[0]

    cursor.execute(query, valores)

    stock_nuevo = int(
        data['stock_actual']
    )

    diferencia = (
        stock_nuevo -
        stock_anterior
    )

    if diferencia != 0:

        query_movimiento = """
            INSERT INTO movimientos_inventario
            (
                id_producto,
                id_usuario,
                tipo_movimiento,
                cantidad,
                motivo
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        valores_movimiento = (

            id_producto,

            1,

            'AJUSTE',

            abs(diferencia),

            f'Ajuste stock {stock_anterior} -> {stock_nuevo}'

        )

        cursor.execute(
            query_movimiento,
            valores_movimiento
        )

    conn.commit()

    cursor.close()
    conn.close()

# Función para eliminar un producto (marcar como inactivo)
def eliminar_producto(id_producto):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT stock_actual
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto = cursor.fetchone()

    stock_actual = producto[0]

    query = """
        UPDATE productos
        SET activo = FALSE
        WHERE id_producto = %s
    """

    cursor.execute(query, (id_producto,))

    query_movimiento = """
        INSERT INTO movimientos_inventario
        (
            id_producto,
            id_usuario,
            tipo_movimiento,
            cantidad,
            motivo
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    valores_movimiento = (

        id_producto,

        1,

        'SALIDA',

        stock_actual,

        'Producto desactivado'

    )

    cursor.execute(
        query_movimiento,
        valores_movimiento
    )

    conn.commit()

    cursor.close()
    conn.close()


def activar_producto(id_producto):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE productos
        SET activo = TRUE
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    conn.commit()

    cursor.close()
    conn.close()

def obtener_resumen_productos():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            COUNT(*) AS total_productos,

            SUM(
                CASE
                    WHEN stock_actual = 0
                    THEN 1
                    ELSE 0
                END
            ) AS agotados,

            SUM(
                CASE
                    WHEN stock_actual > 0
                    AND stock_actual <= stock_minimo
                    THEN 1
                    ELSE 0
                END
            ) AS stock_bajo

        FROM productos
        WHERE activo = TRUE
    """

    cursor.execute(query)

    resumen = cursor.fetchone()

    cursor.close()
    conn.close()

    return resumen