from flask import Blueprint, request
from models import db, Pedido

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return {
        'pedidos': [
            {
                'id_pedido': p.id_pedido,
                'id_usuario': p.id_usuario,
                'fecha_pedido': p.fecha_pedido.isoformat() if p.fecha_pedido else None,
                'total': float(p.total)
            } for p in pedidos
        ]
    }

@pedidos_bp.route('/pedidos', methods=['POST'])
def crear_pedido():
    data = request.json
    pedido = Pedido(
        id_usuario=data['id_usuario'],
        fecha_pedido=data.get('fecha_pedido'),
        total=data['total']
    )
    db.session.add(pedido)
    db.session.commit()
    return {'mensaje': 'Pedido creado', 'id_pedido': pedido.id_pedido}, 201
