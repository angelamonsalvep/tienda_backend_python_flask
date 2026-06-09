# Especificación: Creación Automatizada de Vistas de Analítica SQL

> **Estado:** Implementado · **Depende de:** 01-configuracion-entorno-db · **Fecha:** 2026-06-09
> **Objetivo:** Asegurar la existencia y estructura de las vistas SQL de analítica (`vista_pedidos_detallados` y `vista_productos_mas_vendidos`) de forma automatizada en la base de datos al iniciar la aplicación Flask.

## Alcance (Scope)

### Qué está incluido
- Definición de las sentencias DDL SQL para las vistas `vista_pedidos_detallados` y `vista_productos_mas_vendidos`.
- Ejecución automática de las sentencias de creación (`CREATE OR REPLACE VIEW`) al arrancar la aplicación Flask (justo después de `db.create_all()`).
- Manejo de excepciones para que fallos no críticos durante la creación de vistas no impidan el arranque del servidor backend.

### Qué NO está incluido
- Uso de migraciones de Alembic/Flask-Migrate para versionar las vistas (se crearán directamente con SQL nativo).
- Creación de vistas materializadas (materialized views) o índices en las vistas (se usarán vistas estándar dinámicas de PostgreSQL).

## Modelo de Datos (Data Model)

Se introducen dos vistas lógicas de base de datos basadas en las tablas existentes (`pedidos`, `detalles_pedido`, `productos`).

### 1. Vista `vista_pedidos_detallados`
Esta vista une la información de pedidos, detalles de pedidos y productos para obtener una fila por cada ítem vendido.
* **Sentencia SQL de creación:**
  ```sql
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
  ```

### 2. Vista `vista_productos_mas_vendidos`
Esta vista agrupa los datos de ventas por producto para obtener totales acumulados históricos.
* **Sentencia SQL de creación:**
  ```sql
  CREATE OR REPLACE VIEW vista_productos_mas_vendidos AS
  SELECT 
      pr.nombre_producto,
      SUM(dp.cantidad) AS total_vendido,
      SUM(dp.cantidad * dp.precio_unitario) AS ingresos_generados
  FROM detalles_pedido dp
  JOIN productos pr ON dp.id_producto = pr.id_producto
  GROUP BY pr.nombre_producto;
  ```

## Plan de Implementación (Implementation Plan)

### Componentes a Modificar

#### [MODIFY] [app.py](file:///c:/Users/usuario/Documents/projects/tienda_backend/app.py)
- Añadir un bloque de inicio bajo el contexto de la aplicación (`app.app_context()`) para ejecutar las sentencias SQL nativas de creación de las vistas.
- Utilizar `db.session.execute(text(sql))` seguido de `db.session.commit()` para cada vista.
- Envolver la creación en un bloque `try-except` para evitar caídas catastróficas si hay problemas con los permisos o con el controlador en bases de datos que no sean PostgreSQL (por ejemplo, SQLite de desarrollo).

---

## Pasos de Implementación

### Paso 1: Definir las sentencias SQL y cargarlas al inicio de la aplicación
- En `app.py`, importar `text` de `sqlalchemy` y `db` de `models`.
- Dentro de un bloque `with app.app_context():`, ejecutar:
  ```python
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
  except Exception as e:
      print(f"Error al crear vistas SQL: {e}")
      db.session.rollback()
  ```

## Criterios de Aceptación

- [ ] Al iniciar la aplicación Flask, el backend ejecuta las sentencias SQL de creación de vistas sin producir excepciones que detengan el arranque.
- [ ] La consulta de prueba en el endpoint `/api/ventas-top` devuelve los productos más vendidos en el rango de días especificado sin lanzar el error `relation "vista_pedidos_detallados" does not exist`.
- [ ] La consulta de prueba en el endpoint `/api/ventas-serie` devuelve las series temporales correctas.

## Decisiones Tomadas y Descartadas

*   **Tomada:** Ejecutar `CREATE OR REPLACE VIEW` en el inicio del backend (`app.app_context()`). Esto garantiza que la base de datos de producción (Supabase) siempre tenga las vistas al día sin necesidad de correr scripts externos.
*   **Descartada:** Usar migraciones complejas de Flask-Migrate/Alembic para las vistas. Las vistas no guardan datos de forma persistente, por lo que recrearlas dinámicamente es más sencillo y menos propenso a errores de migración.

## Riesgos Identificados

*   **Riesgo:** Si las tablas `pedidos`, `detalles_pedido` o `productos` no se han creado en el momento en que se intenta crear la vista, la base de datos lanzará un error.
    *   *Mitigación:* Nos aseguraremos de que las vistas se creen inmediatamente después de inicializar la app y de llamar a `db.create_all()` en caso de ser necesario, o manejaremos la excepción de forma silenciosa para que no detenga el servidor.
