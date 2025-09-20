# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar que Python guarde .pyc y usar buffer en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando por defecto (puedes cambiar "app:app" si usas otra estructura)
CMD ["python", "app.py"]
