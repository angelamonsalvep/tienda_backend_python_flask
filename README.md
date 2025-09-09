# Tienda Backend

Backend para una tienda usando Flask y SQLAlchemy.

## Estructura del proyecto

- `app.py`: arranque de la aplicación y registro de rutas.
- `models.py`: definición de los modelos de la base de datos.
- `config.py`: configuración de la base de datos.
- `routes/`: rutas para productos, usuarios, pedidos y detalles de pedido.
- `requirements.txt`: dependencias del proyecto.

## Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configura la variable de entorno `DATABASE_URL` con la URL de tu base de datos PostgreSQL.

## Inicializar la base de datos

En un entorno interactivo de Python:
```python
from app import app
from models import db
with app.app_context():
    db.create_all()
```

## Ejecutar el servidor

```bash
python app.py
```

## Endpoints principales

- `GET /productos` — Listar productos
- `POST /productos` — Crear producto
- `GET /usuarios` — Listar usuarios
- `POST /usuarios` — Crear usuario
- `GET /pedidos` — Listar pedidos
- `POST /pedidos` — Crear pedido
- `GET /detalles_pedido` — Listar detalles de pedido
- `POST /detalles_pedido` — Crear detalle de pedido

## Ejemplo de petición para crear producto

```json
{
  "nombre_producto": "Producto X",
  "imagen_url": "https://via.placeholder.com/150",
  "descripcion": "Descripción del producto X",
  "precio": 99.99
}
```
