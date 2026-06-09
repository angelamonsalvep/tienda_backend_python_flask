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

@app.route('/')
def bienvenida():
    return {'mensaje': 'Bienvenido a la API de Tienda Backend'}, 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

