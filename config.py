import os
from urllib.parse import urlparse

# Obtener URL de base de datos y normalizar el protocolo para SQLAlchemy 2.x
db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/minitienda')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
elif db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

# Determinar si el host es local (localhost, 127.0.0.1 o 'db' para docker-compose)
try:
    parsed = urlparse(db_url)
    host = parsed.hostname or ''
except Exception:
    host = ''

is_local = host in ('localhost', '127.0.0.1', 'db') or not host

class Config:
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Aplicar sslmode=require si la base de datos es externa (ej. Render)
    if not is_local:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }

