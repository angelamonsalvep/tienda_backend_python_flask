from flask import Flask
from config import Config
from models import db
from routes.productos import productos_bp
from routes.usuarios import usuarios_bp
from routes.pedidos import pedidos_bp
from routes.detalles_pedido import detalles_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registrar blueprints
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalles_bp)

if __name__ == '__main__':
    app.run(debug=True)
