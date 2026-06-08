from app.database.connection import get_connection

def obtener_proveedores():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM proveedores
        ORDER BY nombre
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return proveedores


def obtener_proveedor_por_id(id_proveedor):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id_proveedor,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    return proveedor


def insertar_proveedor(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO proveedores
        (
            nombre,
            telefono,
            email
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """,
        (
            data['nombre'],
            data['telefono'],
            data['email']
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def actualizar_proveedor(
    id_proveedor,
    data
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE proveedores
        SET
            nombre=%s,
            telefono=%s,
            email=%s
        WHERE id_proveedor=%s
        """,
        (
            data['nombre'],
            data['telefono'],
            data['email'],
            id_proveedor
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def desactivar_proveedor(
    id_proveedor
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE proveedores
        SET activo = FALSE
        WHERE id_proveedor = %s
        """,
        (id_proveedor,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def activar_proveedor(id_proveedor):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE proveedores
        SET activo = TRUE
        WHERE id_proveedor = %s
        """,
        (id_proveedor,)
    )

    conn.commit()

    cursor.close()
    conn.close()