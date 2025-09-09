from flask import Blueprint, request
from models import db, DetallePedido

detalles_bp = Blueprint('detalles_pedido', __name__)

@detalles_bp.route('/detalles_pedido', methods=['GET'])
def get_detalles():
    detalles = DetallePedido.query.all()
    return {
        'detalles_pedido': [
            {
                'id_detalle': d.id_detalle,
                'id_pedido': d.id_pedido,
                'id_producto': d.id_producto,
                'cantidad': d.cantidad,
                'precio_unitario': float(d.precio_unitario)
            } for d in detalles
        ]
    }

@detalles_bp.route('/detalles_pedido', methods=['POST'])
def crear_detalle():
    data = request.json
    detalle = DetallePedido(
        id_pedido=data['id_pedido'],
        id_producto=data['id_producto'],
        cantidad=data['cantidad'],
        precio_unitario=data['precio_unitario']
    )
    db.session.add(detalle)
    db.session.commit()
    return {'mensaje': 'Detalle creado', 'id_detalle': detalle.id_detalle}, 201
