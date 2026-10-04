from flask import jsonify, request

from ..errors import error, required
from ..extensions import db
from ..models import Cliente, Pedido, Producto
from . import api_bp


@api_bp.get("/pedidos")
def listar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()

    return jsonify([
        pedido.to_dict()
        for pedido in pedidos
    ])


@api_bp.get("/pedidos/<int:pedido_id>")
def obtener_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)

    return jsonify(pedido.to_dict())


@api_bp.post("/pedidos")
def crear_pedido():
    data = request.get_json(silent=True) or {}

    missing = required(
        data,
        ["cliente_id", "producto_id", "cantidad"],
    )

    if missing:
        return error(
            "Faltan campos obligatorios",
            details=missing,
        )

    try:
        cliente_id = int(data["cliente_id"])
        producto_id = int(data["producto_id"])
        cantidad = int(data["cantidad"])
    except (TypeError, ValueError):
        return error(
            "Los IDs y la cantidad deben ser enteros"
        )

    if cantidad <= 0:
        return error(
            "La cantidad debe ser mayor que cero"
        )

    cliente = db.session.get(Cliente, cliente_id)

    if not cliente:
        return error(
            "El cliente no existe",
            404,
        )

    producto = db.session.get(Producto, producto_id)

    if not producto:
        return error(
            "El producto no existe",
            404,
        )

    if cantidad > producto.stock:
        return error(
            "No hay suficiente stock",
            409,
        )

    pedido = Pedido(
        cliente_id=cliente_id,
        producto_id=producto_id,
        cantidad=cantidad,
        estado=data.get(
            "estado",
            "pendiente",
        ),
    )

    producto.stock -= cantidad

    db.session.add(pedido)
    db.session.commit()

    return jsonify(pedido.to_dict()), 201


@api_bp.put("/pedidos/<int:pedido_id>")
def actualizar_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)

    data = request.get_json(silent=True) or {}

    missing = required(
        data,
        ["cliente_id", "producto_id", "cantidad"],
    )

    if missing:
        return error(
            "Faltan campos obligatorios",
            details=missing,
        )

    pedido.cliente_id = int(data["cliente_id"])
    pedido.producto_id = int(data["producto_id"])
    pedido.cantidad = int(data["cantidad"])

    if "estado" in data:
        pedido.estado = data["estado"]

    db.session.commit()

    return jsonify(pedido.to_dict())


@api_bp.delete("/pedidos/<int:pedido_id>")
def eliminar_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)

    db.session.delete(pedido)
    db.session.commit()

    return "", 204