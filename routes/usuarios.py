from flask import Blueprint, request
from models import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return {
        'usuarios': [
            {
                'id_usuario': u.id_usuario,
                'nombre_usuario': u.nombre_usuario,
                'email': u.email
            } for u in usuarios
        ]
    }

@usuarios_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    usuario = Usuario(
        nombre_usuario=data['nombre_usuario'],
        email=data['email']
    )
    db.session.add(usuario)
    db.session.commit()
    return {'mensaje': 'Usuario creado', 'id_usuario': usuario.id_usuario}, 201
