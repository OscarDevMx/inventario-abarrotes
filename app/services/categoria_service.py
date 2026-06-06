from app.database.connection import get_connection


# Funciones para manejar las categorías de productos
def obtener_categorias():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            id_categoria,
            nombre_categoria,
            activo,
            fecha_creacion
        FROM categorias
        ORDER BY nombre_categoria
    """)

    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return categorias

# Funcion para insertar una nueva categoria en la base de datos
def insertar_categoria(nombre_categoria):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO categorias
        (
            nombre_categoria
        )
        VALUES
        (
            %s
        )
        """,
        (nombre_categoria,)
    )

    conn.commit()

    cursor.close()
    conn.close()

# Función para actualizar una categoría existente en la base de datos
def actualizar_categoria(
    id_categoria,
    nombre_categoria
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE categorias
        SET nombre_categoria = %s
        WHERE id_categoria = %s
        """,
        (
            nombre_categoria,
            id_categoria
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

# Función para eliminar una categoría (marcar como inactiva)
def desactivar_categoria(id_categoria):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE categorias
        SET activo = FALSE
        WHERE id_categoria = %s
        """,
        (id_categoria,)
    )

    conn.commit()

    cursor.close()
    conn.close()

# Función para obtener una categoría por su ID
def obtener_categoria_por_id(id_categoria):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM categorias
        WHERE id_categoria = %s
        """,
        (id_categoria,)
    )

    categoria = cursor.fetchone()

    cursor.close()
    conn.close()

    return categoria

# Función para reactivar una categoría (marcar como activa)
def activar_categoria(id_categoria):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE categorias
        SET activo = TRUE
        WHERE id_categoria = %s
        """,
        (id_categoria,)
    )

    conn.commit()

    cursor.close()
    conn.close()