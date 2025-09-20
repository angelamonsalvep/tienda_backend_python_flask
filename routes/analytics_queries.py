"""
Constantes de consultas SQL para analítica de productos y ventas.
"""

# Consulta para obtener los productos top por ventas o ingresos en un rango de días
TOP_PRODUCTOS_QUERY = """
    SELECT nombre_producto, SUM(cantidad) AS cantidad, SUM(subtotal) AS subtotal
    FROM vista_pedidos_detallados
    WHERE fecha_pedido >= CURRENT_DATE - INTERVAL '{days} days'
    GROUP BY nombre_producto
    ORDER BY {metric} DESC
    LIMIT :limit
"""

# Consulta para obtener la serie temporal de ventas/ingresos por producto y fecha
DETALLE_SERIE_QUERY = """
    SELECT fecha_pedido::date AS fecha, nombre_producto,
           SUM(cantidad) AS cantidad, SUM(subtotal) AS subtotal
    FROM vista_pedidos_detallados
    WHERE fecha_pedido >= CURRENT_DATE - INTERVAL '{days} days'
      AND nombre_producto IN ({in_clause})
    GROUP BY fecha, nombre_producto
    ORDER BY fecha ASC, nombre_producto ASC
"""

# Consulta para obtener los productos más vendidos o con más ingresos (vista agregada)
VENTAS_TOP_QUERY = """
    SELECT nombre_producto, total_vendido, ingresos_generados
    FROM vista_productos_mas_vendidos
    ORDER BY {metric} DESC
    LIMIT :limit
"""
