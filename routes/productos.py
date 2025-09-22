from flask import Blueprint, request
from models import db, Producto
import json

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.filter_by(activo=True).all()
    return {
        'productos': [
            {
                'id_producto': p.id_producto,
                'nombre_producto': p.nombre_producto,
                'imagen_url': json.loads(p.imagen_url) if p.imagen_url else [],
                'descripcion': p.descripcion,
                'precio': float(p.precio)
            } for p in productos
        ]
    }

# Endpoint para obtener producto por id
@productos_bp.route('/productos/<int:id_producto>', methods=['GET'])
def get_producto(id_producto):
    producto = Producto.query.get(id_producto)
    if not producto or not producto.activo:
        return {'mensaje': 'Producto no encontrado'}, 404
    return {
        'id_producto': producto.id_producto,
        'nombre_producto': producto.nombre_producto,
        'imagen_url': json.loads(producto.imagen_url) if producto.imagen_url else [],
        'descripcion': producto.descripcion,
        'precio': float(producto.precio)
    }

@productos_bp.route('/productos', methods=['POST'])
def crear_producto():
    print('Datos recibidos en POST /productos:', request.json)
    data = request.json
    imagenes = data.get('imagen_url', [])
    # Validar que cada imagen sea un objeto con tipo y url
    if not isinstance(imagenes, list):
        imagenes = [imagenes] if imagenes else []
    imagenes = [img for img in imagenes if isinstance(img, dict) and 'url' in img and 'tipo' in img]
    producto = Producto(
        nombre_producto=data['nombre_producto'],
        imagen_url=json.dumps(imagenes),
        descripcion=data.get('descripcion'),
        precio=data['precio']
    )
    db.session.add(producto)
    db.session.commit()
    return {'mensaje': 'Producto creado', 'id_producto': producto.id_producto}, 201

# Endpoint para editar producto
@productos_bp.route('/productos/<int:id_producto>', methods=['PUT', 'PATCH'])
def editar_producto(id_producto):
    print(f'Datos recibidos en PUT/PATCH /productos/{id_producto}:', request.json)
    data = request.json
    producto = Producto.query.get(id_producto)
    if not producto:
        return {'mensaje': 'Producto no encontrado'}, 404
    producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
    imagenes = data.get('imagen_url')
    # Si no se envía imagen_url, mantener las actuales
    if imagenes is None:
        imagenes = json.loads(producto.imagen_url) if producto.imagen_url else []
    # Si se envía como string, intentar decodificar
    elif isinstance(imagenes, str):
        try:
            imagenes = json.loads(imagenes)
        except Exception:
            imagenes = []
    # Si no es lista, convertir a lista
    if not isinstance(imagenes, list):
        imagenes = [imagenes] if imagenes else []
    # Validar estructura de cada imagen
    imagenes = [img for img in imagenes if isinstance(img, dict) and 'url' in img and 'tipo' in img]
    producto.imagen_url = json.dumps(imagenes)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    db.session.commit()
    return {'mensaje': 'Producto actualizado', 'id_producto': producto.id_producto}

# Endpoint para eliminar producto
@productos_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    print(f'Recibida solicitud DELETE /productos/{id_producto}')
    producto = Producto.query.get(id_producto)
    if not producto:
        return {'mensaje': 'Producto no encontrado'}, 404
    if not producto.activo:
        return {'mensaje': 'El producto ya está inactivo', 'id_producto': id_producto}, 400
    producto.activo = False
    db.session.commit()
    return {'mensaje': 'Producto marcado como eliminado', 'id_producto': id_producto}
