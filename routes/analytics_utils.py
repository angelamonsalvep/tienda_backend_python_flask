"""
Funciones utilitarias para consultas analíticas de productos y ventas.
"""

from models import db
from sqlalchemy import text
from .analytics_queries import TOP_PRODUCTOS_QUERY, DETALLE_SERIE_QUERY

def get_top_productos(days, metric, limit):
    """
    Ejecuta la consulta para obtener los productos top por ventas o ingresos.
    Retorna una lista de diccionarios con nombre_producto, cantidad y subtotal.
    """
    query_str = TOP_PRODUCTOS_QUERY.format(days=days, metric=metric)
    query = text(query_str)
    result = db.session.execute(query, {"limit": limit})
    return [dict(row) for row in result.mappings()]


def get_serie_detalle(days, metric, top_productos):
    """
    Ejecuta la consulta para obtener la serie temporal de ventas/ingresos por producto y fecha.
    Retorna una lista de diccionarios con fecha, nombre_producto, cantidad y subtotal.
    """
    in_clause = ",".join([f"'{p}'" for p in top_productos])
    detalle_query_str = DETALLE_SERIE_QUERY.format(days=days, in_clause=in_clause)
    detalle_query = text(detalle_query_str)
    detalle_result = db.session.execute(detalle_query)
    return list(detalle_result.mappings())
