inventario-abarrotes/
│
├── app/
│   │
│   ├── routes/
│   │   └── productos.py
│   │   └── ventas.py
│   │   └── reportes.py
│   │   └── movimientos.py
│   │   └── categorias.py
│   │   └── proveedores.py
│   │
│   ├── services/
│   │   └── producto_service.py
│   │   └── venta_service.py
│   │   └── reporte_service.py
│   │   └── movimiento_service.py
│   │   └── categoria_service.py
│   │   └── proveedor_service.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── productos/
│   │   │   ├── listar.html
│   │   │   ├── crear.html
│   │   │   └── editar.html
│   │   └── ventas/
│   │   │   └── pos.html
│   │   └── reportes/
│   │       └── dashboard.html
│   │   └── movimientos/
│   │       └── listar.html
│   │   └── categorias/
│   │       └── listar.html
│   │   └── proveedores/
│   │       └── listar.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │
│   └── __init__.py
│
├── config.py
├── run.py
├── requirements.txt
└── README.md