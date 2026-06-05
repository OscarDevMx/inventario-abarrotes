import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2026",
        database="inventario_abarrotes"
    )