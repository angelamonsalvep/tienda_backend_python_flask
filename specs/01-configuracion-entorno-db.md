# Especificación: Configuración de Entorno y Conexión Segura a PostgreSQL

> **Estado:** Aprobado · **Depende de:** Ninguna · **Fecha:** 2026-06-09
> **Objetivo:** Configurar el backend para cargar variables de entorno locales desde `.env.local` y establecer una conexión segura (SSL) compatible con Render y PostgreSQL.

## Alcance (Scope)

### Qué está incluido
- Soporte para archivos `.env.local` (desarrollo local) y `.env` (producción/Render), asegurando que `.env.local` tenga prioridad.
- Exclusión de `.env.local` en el archivo `.gitignore` para prevenir fugas de credenciales locales en el repositorio.
- Corrección automática del protocolo de conexión de base de datos (`postgres://` a `postgresql+psycopg2://`) en la configuración del backend.
- Conexión segura (SSL) activa de manera condicional: se aplicará `sslmode=require` mediante `connect_args` si el host de la base de datos no es local (`localhost` o `127.0.0.1`).
- Creación de un archivo `.env.example` para documentar la estructura de variables requerida.

### Qué NO está incluido
- Configuración avanzada de orígenes CORS o certificados SSL personalizados para el servidor web (solo aplica a la conexión del driver de PostgreSQL).
- Automatización del despliegue en Render (Render obtiene las variables directamente de su panel de administración).

## Modelo de Datos (Data Model)

Esta configuración no introduce nuevos modelos, tablas o estructuras de datos persistentes en la base de datos de la aplicación.

## Plan de Implementación (Implementation Plan)

### Paso 1: Configurar exclusiones en Git
- Modificar el archivo `.gitignore` del backend para añadir `.env.local`.

### Paso 2: Crear plantilla de variables de entorno
- Crear el archivo `.env.example` en la raíz del backend con los campos:
  - `FLASK_ENV`
  - `SECRET_KEY`
  - `DATABASE_URL`

### Paso 3: Carga priorizada de entornos en `app.py`
- Actualizar la carga de variables en `app.py` para que lea primero `.env.local` si existe, y si no, caiga en `.env` (o lea ambos con prioridad para el primero).

### Paso 4: Ajustar la URI de conexión y parámetros SSL en `config.py`
- Obtener `DATABASE_URL` desde el entorno.
- Aplicar la corrección para convertir `postgres://` en `postgresql+psycopg2://`.
- Analizar el host de la URL de conexión. Si no contiene `localhost`, `127.0.0.1` o `db` (host de docker-compose), añadir la opción de motor SQLAlchemy:
  ```python
  SQLALCHEMY_ENGINE_OPTIONS = {
      "connect_args": {
          "sslmode": "require"
      }
  }
  ```
- Asignar la URI limpia a `SQLALCHEMY_DATABASE_URI`.

## Criterios de Aceptación

- [ ] El archivo `.gitignore` incluye la línea `.env.local`.
- [ ] El archivo `.env.example` existe y sirve como plantilla documentada.
- [ ] La aplicación lee variables de `.env.local` en desarrollo local con éxito y con prioridad sobre cualquier otra.
- [ ] Al iniciar la aplicación con una URL de base de datos que comience con `postgres://`, esta se reescribe a `postgresql+psycopg2://` sin lanzar errores de esquema.
- [ ] Al configurar una URL de base de datos que no sea local (por ejemplo, la de producción en Render), se adjunta la configuración `sslmode=require` de forma segura.

## Decisiones Tomadas y Descartadas
*   **Tomada:** Usar `.env.local` con prioridad sobre `.env`. Esto mantiene el patrón consistente con la configuración del frontend de MiniTienda y previene la subida accidental de credenciales locales.
*   **Tomada:** Reemplazo dinámico de `postgres://` en el código. Esto nos ahorra tener que editar manualmente la URL que Render genera automáticamente, evitando errores de SQLAlchemy.
*   **Tomada:** Detección de host dinámico para aplicar SSL (`sslmode=require`). Esto evita tener que usar variables adicionales para encender/apagar SSL según el ambiente.
*   **Descartada:** Forzar SSL en todo momento. Se descartó para no obligar a los desarrolladores locales a configurar certificados SSL en sus bases de datos PostgreSQL de desarrollo.

## Riesgos Identificados
*   **Riesgo:** Si un desarrollador usa un host local que no contiene `localhost` o `127.0.0.1` (por ejemplo, una IP de red local o un alias personalizado), el backend intentará conectarse con SSL y fallará.
    *   *Mitigación:* Se documenta en el `.env.example` y en el plan de pruebas que el host local debe ser `localhost`, `127.0.0.1` o `db` (para Docker).
