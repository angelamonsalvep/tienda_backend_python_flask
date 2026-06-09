from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar .env.local con prioridad sobre .env antes de importar otros módulos
load_dotenv('.env.local')
load_dotenv('.env')

from config import Config
from models import db
from routes.productos import productos_bp
from routes.usuarios import usuarios_bp
from routes.pedidos import pedidos_bp
from routes.detalles_pedido import detalles_bp
from routes.analitica import analitica_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configuración CORS global (aceptar todo durante pruebas)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Registrar blueprints
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalles_bp)
app.register_blueprint(analitica_bp)

# Crear vistas de analítica automáticamente en el arranque
with app.app_context():
    from sqlalchemy import text
    try:
        # 1. Vista pedidos detallados
        db.session.execute(text("""
            CREATE OR REPLACE VIEW vista_pedidos_detallados AS
            SELECT 
                p.id_pedido,
                p.fecha_pedido,
                pr.id_producto,
                pr.nombre_producto,
                dp.cantidad,
                dp.precio_unitario,
                (dp.cantidad * dp.precio_unitario) AS subtotal
            FROM detalles_pedido dp
            JOIN pedidos p ON dp.id_pedido = p.id_pedido
            JOIN productos pr ON dp.id_producto = pr.id_producto;
        """))
        # 2. Vista productos más vendidos
        db.session.execute(text("""
            CREATE OR REPLACE VIEW vista_productos_mas_vendidos AS
            SELECT 
                pr.nombre_producto,
                SUM(dp.cantidad) AS total_vendido,
                SUM(dp.cantidad * dp.precio_unitario) AS ingresos_generados
            FROM detalles_pedido dp
            JOIN productos pr ON dp.id_producto = pr.id_producto
            GROUP BY pr.nombre_producto;
        """))
        db.session.commit()
        print("Vistas SQL de analítica creadas o actualizadas exitosamente.")
    except Exception as e:
        print(f"Error al crear vistas SQL: {e}")
        db.session.rollback()


@app.route('/')
def bienvenida():
    return {'mensaje': 'Bienvenido a la API de Tienda Backend'}, 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

