from flask import Blueprint, request
from models import db, Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return {
        'productos': [
            {
                'id_producto': p.id_producto,
                'nombre_producto': p.nombre_producto,
                'imagen_url': p.imagen_url,
                'descripcion': p.descripcion,
                'precio': float(p.precio)
            } for p in productos
        ]
    }

@productos_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.json
    producto = Producto(
        nombre_producto=data['nombre_producto'],
        imagen_url=data.get('imagen_url'),
        descripcion=data.get('descripcion'),
        precio=data['precio']
    )
    db.session.add(producto)
    db.session.commit()
    return {'mensaje': 'Producto creado', 'id_producto': producto.id_producto}, 201
