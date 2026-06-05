from app.database.connection import get_connection
from datetime import datetime


# Buscar producto por código de barras
def buscar_producto_codigo(codigo_barras):

    conexion = get_connection()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""

        SELECT
            id_producto,
            nombre,
            precio,
            stock_actual
        FROM productos
        WHERE codigo_barras = %s
        AND activo = 1

    """, (codigo_barras,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return producto


# Obtener tipos de pago para dropdown
def obtener_tipos_pago():

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT

            id_tipo_pago,
            nombre_pago

        FROM tipo_pago

        ORDER BY id_tipo_pago

    """)

    tipos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return tipos


# Obtener nombre de tipo de pago para ticket
def obtener_nombre_pago(

    id_tipo_pago

):

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT nombre_pago

        FROM tipo_pago

        WHERE id_tipo_pago = %s

    """, (

        id_tipo_pago,

    ))

    pago = cursor.fetchone()

    cursor.close()
    conexion.close()

    return pago['nombre_pago']


# Obtener stock actual para validación
def obtener_stock_actual(

    cursor,
    id_producto

):

    cursor.execute("""

        SELECT stock_actual

        FROM productos

        WHERE id_producto = %s

    """, (

        id_producto,

    ))

    resultado = cursor.fetchone()

    return resultado[0]

# Agregar al carrito
def guardar_venta(carrito, id_tipo_pago):

    conexion = get_connection()

    cursor = conexion.cursor()

    try:

        conexion.start_transaction()

        # Total

        total = sum(
            item['subtotal']
            for item in carrito
        )

        subtotal = total

        # Folio simple temporal

        folio = (
            'V-'
            +
            datetime.now().strftime(
                '%Y%m%d%H%M%S'
            )
        )

        id_usuario = None

        # INSERT venta

        cursor.execute("""

            INSERT INTO ventas (

                folio,
                subtotal,
                total,
                id_tipo_pago,
                id_usuario

            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """, (

            folio,
            subtotal,
            total,
            id_tipo_pago,
            id_usuario

        ))

        id_venta = cursor.lastrowid

        # DETALLE + STOCK + MOV

        for item in carrito:
            stock_bd = obtener_stock_actual(

                cursor,

                item['id_producto']

            )

            if item['cantidad'] > stock_bd:

                raise Exception(

                    f"Stock insuficiente para "

                    f"{item['nombre']} "

                    f"(Disponible: {stock_bd})"

                )

            # detalle

            cursor.execute("""

                INSERT INTO detalle_venta(

                    id_venta,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal

                )
                VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

            """, (

                id_venta,
                item['id_producto'],
                item['cantidad'],
                item['precio'],
                item['subtotal']

            ))

            # descontar stock

            cursor.execute("""

                UPDATE productos
                SET stock_actual =
                    stock_actual - %s
                WHERE id_producto = %s

            """, (

                item['cantidad'],
                item['id_producto']

            ))

            # movimiento

            cursor.execute("""

                INSERT INTO
                movimientos_inventario(

                    id_producto,
                    id_venta,
                    id_usuario,
                    tipo_movimiento,
                    cantidad,
                    motivo

                )
                VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

            """, (

                item['id_producto'],
                id_venta,
                id_usuario,
                'VENTA',
                item['cantidad'],
                f'VENTA {folio}'

            ))

        conexion.commit()

        return {

            'ok': True,
            
            'id_venta': id_venta,

            'folio': folio,

            'total': total,

            'id_tipo_pago': id_tipo_pago

        }

    except Exception as e:

        conexion.rollback()

        return {

            'ok': False,
            'error': str(e)

        }

    finally:

        cursor.close()
        conexion.close()


# Obtener datos para ticket
def obtener_ticket(id_venta):

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    # encabezado

    cursor.execute("""

        SELECT

            v.id_venta,
            v.folio,
            v.fecha_venta,
            v.subtotal,
            v.total,
            tp.nombre_pago

        FROM ventas v

        INNER JOIN tipo_pago tp
            ON v.id_tipo_pago =
               tp.id_tipo_pago

        WHERE v.id_venta = %s

    """, (

        id_venta,

    ))

    venta = cursor.fetchone()

    # detalle

    cursor.execute("""

        SELECT

            p.nombre,
            dv.cantidad,
            dv.precio_unitario,
            dv.subtotal

        FROM detalle_venta dv

        INNER JOIN productos p

            ON dv.id_producto =
               p.id_producto

        WHERE dv.id_venta = %s

    """, (

        id_venta,

    ))

    detalle = cursor.fetchall()

    cursor.close()
    conexion.close()

    return venta, detalle

# Obtener historial de ventas para reporte
def obtener_historial_ventas():

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT

            v.id_venta,
            v.folio,
            v.fecha_venta,
            tp.nombre_pago,
            v.total

        FROM ventas v

        INNER JOIN tipo_pago tp

            ON v.id_tipo_pago =
               tp.id_tipo_pago

        ORDER BY
            v.fecha_venta DESC

    """)

    ventas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return ventas