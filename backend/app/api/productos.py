from flask import jsonify, request
from ..errors import error, required
from ..extensions import db
from ..models import Producto
from . import api_bp


@api_bp.get("/productos")
def listar_productos():
    productos = Producto.query.order_by(Producto.id.desc()).all()

    return jsonify([
        producto.to_dict()
        for producto in productos
    ])


@api_bp.get("/productos/<int:producto_id>")
def obtener_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)

    return jsonify(producto.to_dict())


@api_bp.post("/productos")
def crear_producto():
    data = request.get_json(silent=True) or {}

    missing = required(
        data,
        ["nombre", "precio", "stock"],
    )

    if missing:
        return error(
            "Faltan campos obligatorios",
            details=missing,
        )

    try:
        precio = float(data["precio"])
        stock = int(data["stock"])
    except (TypeError, ValueError):
        return error(
            "precio debe ser numérico y stock debe ser entero"
        )

    if precio < 0:
        return error("El precio no puede ser negativo")

    if stock < 0:
        return error("El stock no puede ser negativo")

    producto = Producto(
        nombre=data["nombre"].strip(),
        descripcion=data.get("descripcion", "").strip(),
        precio=precio,
        stock=stock,
        activo=data.get("activo", True),
    )

    db.session.add(producto)
    db.session.commit()

    return jsonify(producto.to_dict()), 201


@api_bp.put("/productos/<int:producto_id>")
def actualizar_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)

    data = request.get_json(silent=True) or {}

    missing = required(
        data,
        ["nombre", "precio", "stock"],
    )

    if missing:
        return error(
            "Faltan campos obligatorios",
            details=missing,
        )

    try:
        precio = float(data["precio"])
        stock = int(data["stock"])
    except (TypeError, ValueError):
        return error(
            "precio debe ser numérico y stock debe ser entero"
        )

    if precio < 0 or stock < 0:
        return error(
            "precio y stock no pueden ser negativos"
        )

    producto.nombre = data["nombre"].strip()
    producto.descripcion = data.get(
        "descripcion",
        "",
    ).strip()
    producto.precio = precio
    producto.stock = stock
    producto.activo = data.get(
        "activo",
        producto.activo,
    )

    db.session.commit()

    return jsonify(producto.to_dict())


@api_bp.delete("/productos/<int:producto_id>")
def eliminar_producto(producto_id):
    producto = db.get_or_404(
        Producto,
        producto_id,
    )

    if producto.pedidos:
        return error(
            "No se puede eliminar un producto con pedidos",
            409,
        )

    db.session.delete(producto)
    db.session.commit()

    return "", 204