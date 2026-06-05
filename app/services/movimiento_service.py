from app.database.connection import get_connection


def obtener_movimientos():

    conexion = get_connection()

    cursor = conexion.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT

            m.id_movimiento,

            m.fecha_movimiento,

            p.nombre AS producto,

            m.tipo_movimiento,

            m.cantidad,

            m.motivo,

            m.id_venta

        FROM movimientos_inventario m

        INNER JOIN productos p

            ON m.id_producto =
               p.id_producto

        ORDER BY

            m.fecha_movimiento DESC

    """)

    movimientos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return movimientos