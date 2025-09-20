

# -----------------------------
# Imports
# -----------------------------
from flask import Blueprint, request, jsonify
from collections import defaultdict, OrderedDict
from .analytics_utils import get_top_productos, get_serie_detalle

# -----------------------------
# Blueprint
# -----------------------------
analitica_bp = Blueprint('analitica', __name__)


# -----------------------------

# -----------------------------


# -----------------------------
# Endpoint: Productos Top
# -----------------------------
@analitica_bp.route('/api/ventas-top', methods=['GET'])
def ventas_top():
    """
    Devuelve los productos más vendidos o con más ingresos en el rango de días.
    Params: days, metric, limit
    """
    try:
        days = int(request.args.get("days", 30))
        metric = request.args.get("metric", "cantidad")
        limit = int(request.args.get("limit", 6))
        if metric not in ("cantidad", "subtotal"):
            metric = "cantidad"
    except Exception:
        return jsonify({"error": "params inválidos"}), 400

    productos = get_top_productos(days, metric, limit)
    return jsonify(productos)

# -----------------------------
# Endpoint: Serie temporal de ventas por producto top
# -----------------------------
@analitica_bp.route('/api/ventas-serie', methods=['GET'])
def ventas_serie():
    """
    Devuelve la serie temporal de ventas o ingresos para los productos top en el rango de días.
    Params: days, metric, top
    """
    try:
        days = int(request.args.get("days", 30))
        metric = request.args.get("metric", "cantidad")
        top_n = int(request.args.get("top", 5))
        if metric not in ("cantidad", "subtotal"):
            metric = "cantidad"
    except Exception:
        return jsonify({"error": "params inválidos"}), 400

    # 1. Obtener productos top
    top_productos_data = get_top_productos(days, metric, top_n)
    top_productos = [row["nombre_producto"] for row in top_productos_data]
    if not top_productos:
        return jsonify({"labels": [], "series": []})

    # 2. Obtener detalle por fecha y producto
    detalle = get_serie_detalle(days, metric, top_productos)

    # 3. Procesar datos para respuesta tipo serie
    by_title = defaultdict(lambda: OrderedDict())
    fechas_set = set()
    for r in detalle:
        f = str(r["fecha"])
        t = r["nombre_producto"]
        val = r[metric]
        fechas_set.add(f)
        by_title[t][f] = float(val or 0.0)

    labels = sorted(list(fechas_set))
    series = []
    for t in top_productos:
        od = by_title.get(t, {})
        data = [float(od.get(f, 0.0)) for f in labels]
        series.append({"titulo": t, "data": data})
    return jsonify({"labels": labels, "series": series})
