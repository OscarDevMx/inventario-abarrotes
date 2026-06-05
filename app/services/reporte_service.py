from app.database.connection import get_connection

# Servicio para el reporte del dashboard
def obtener_kpis_dashboard():

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    # ventas

    cursor.execute("""

        SELECT

            COUNT(*) total_ventas,

            IFNULL(
                SUM(total),
                0
            ) ingresos,

            IFNULL(
                AVG(total),
                0
            ) ticket_promedio

        FROM ventas

    """)

    ventas = cursor.fetchone()

    # productos activos

    cursor.execute("""

        SELECT COUNT(*)
        total_productos

        FROM productos

        WHERE activo = 1

    """)

    productos = cursor.fetchone()

    # productos vendidos

    cursor.execute("""

        SELECT

            IFNULL(
                SUM(cantidad),
                0
            ) productos_vendidos

        FROM detalle_venta

    """)

    productos_vendidos = cursor.fetchone()

    cursor.close()
    conexion.close()

    return {

        'ventas_totales':
            ventas['total_ventas'],

        'ingresos':
            ventas['ingresos'],

        'ticket_promedio':
            ventas['ticket_promedio'],

        'productos_vendidos':
            productos_vendidos['productos_vendidos']

    }

# Servicio para obtener las últimas ventas y productos con stock crítico
def obtener_ultimas_ventas():

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT

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

        LIMIT 5

    """)

    ventas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return ventas



def obtener_top_productos():

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT

            p.nombre,

            SUM(
                dv.cantidad
            ) cantidad_vendida

        FROM detalle_venta dv

        INNER JOIN productos p

            ON dv.id_producto =
               p.id_producto

        GROUP BY

            p.id_producto,
            p.nombre

        ORDER BY

            cantidad_vendida DESC

        LIMIT 5

    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return productos