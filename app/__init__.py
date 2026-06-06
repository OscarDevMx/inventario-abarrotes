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

        # KPI Productos

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM productos
            WHERE activo = 1

        """)

        total_productos = cursor.fetchone()['total']

        # KPI Stock Bajo

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM productos
            WHERE activo = 1
            AND stock_actual <= stock_minimo

        """)

        stock_bajo = cursor.fetchone()['total']

        # KPI Categorias

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM categorias

        """)

        total_categorias = cursor.fetchone()['total']

        # KPI Proveedores

        cursor.execute("""

            SELECT COUNT(*) AS total
            FROM proveedores

        """)

        total_proveedores = cursor.fetchone()['total']

        # Tabla stock bajo

        cursor.execute("""

            SELECT
                nombre,
                stock_actual,
                stock_minimo
            FROM productos
            WHERE activo = 1
            AND stock_actual <= stock_minimo
            ORDER BY stock_actual ASC
            LIMIT 10

        """)

        productos_stock_bajo = cursor.fetchall()

        cursor.close()
        conexion.close()

        return render_template(

            'home.html',

            total_productos=total_productos,
            stock_bajo=stock_bajo,
            total_categorias=total_categorias,
            total_proveedores=total_proveedores,
            productos_stock_bajo=productos_stock_bajo

        )

    return app