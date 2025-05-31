from flask import session
from app.controllers.product_controller import obtener_producto_por_id

def agregar_a_carrito(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return False, "Producto no encontrado."
    item = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': float(producto.precio),
        'categoria': producto.categoria
    }
    carrito = session.get('carrito', [])
    carrito.append(item)
    session['carrito'] = carrito
    return True, f'Se agregó "{producto.nombre}" al carrito.'

def quitar_de_carrito(indice):
    carrito = session.get('carrito', [])
    if 0 <= indice < len(carrito):
        producto_quitado = carrito[indice]['nombre']
        carrito.pop(indice)
        session['carrito'] = carrito
        return True, f'Se eliminó "{producto_quitado}" del carrito.'
    return False, "Índice inválido."

def obtener_carrito():
    carrito = session.get('carrito', [])
    total = sum(float(p['precio']) for p in carrito)
    return carrito, total

def limpiar_carrito():
    session['carrito'] = []