from flask import Flask, render_template
from app.database.connection import get_connection
from app.routes.productos import productos_bp
from app.routes.ventas import ventas_bp
from app.routes.reportes import (reportes_bp)
from app.routes.movimientos import (movimientos_bp)
from app.routes.categorias import (categorias_bp)
from app.routes.proveedores import (proveedores_bp)



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.register_blueprint(ventas_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(movimientos_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(proveedores_bp)
    
    try:
        conn = get_connection()
        print("Conexión MySQL OK")
        conn.close()
    except Exception as e:
        print("Error conexión:", e)

    @app.route('/')
    def home():

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        # KPI Productos Activos

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM productos
            WHERE activo = 1

        """)

        productos_activos = cursor.fetchone()['total']

        # KPI Stock Bajo

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM productos
            WHERE activo = 1
            AND stock_actual > 0
            AND stock_actual <= stock_minimo

        """)

        stock_bajo = cursor.fetchone()['total']

        # KPI Stock Agotado

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM productos
            WHERE activo = 1
            AND stock_actual = 0

        """)

        stock_agotado = cursor.fetchone()['total']

        # KPI Productos Inactivos

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM productos
            WHERE activo = 0

        """)

        productos_inactivos = cursor.fetchone()['total']

        # Tabla Stock Bajo

        cursor.execute("""

            SELECT
                nombre,
                stock_actual,
                stock_minimo
            FROM productos
            WHERE activo = 1
            AND stock_actual > 0
            AND stock_actual <= stock_minimo
            ORDER BY stock_actual ASC
            LIMIT 10

        """)

        productos_stock_bajo = cursor.fetchall()

        # Tabla Stock Agotado

        cursor.execute("""

            SELECT
                nombre,
                stock_actual
            FROM productos
            WHERE activo = 1
            AND stock_actual = 0
            ORDER BY nombre
            LIMIT 10

        """)

        productos_agotados = cursor.fetchall()

        cursor.close()
        conexion.close()

        return render_template(

            'home.html',

            productos_activos=productos_activos,
            stock_bajo=stock_bajo,
            stock_agotado=stock_agotado,
            productos_inactivos=productos_inactivos,
            productos_stock_bajo=productos_stock_bajo,
            productos_agotados=productos_agotados
        )

    return app