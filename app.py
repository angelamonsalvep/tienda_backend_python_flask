from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from models import db
from routes.productos import productos_bp
from routes.usuarios import usuarios_bp
from routes.pedidos import pedidos_bp
from routes.detalles_pedido import detalles_bp

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Permitir solicitudes CORS desde el frontend
CORS(app, origins=["http://localhost:5173"])

# Registrar blueprints
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalles_bp)
@app.route('/')
def bienvenida():
    return {'mensaje': 'Bienvenido a la API de Tienda Backend'}, 200

if __name__ == '__main__':
    app.run(debug=True)
