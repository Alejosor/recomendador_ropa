from flask import session
from app.controllers.product_controller import obtener_producto_por_id

def agregar_a_carrito(producto_id, cantidad=1):
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return False, "Producto no encontrado."
    
    # Validar cantidad
    if cantidad <= 0:
        cantidad = 1
        
    item = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': float(producto.precio),
        'categoria': producto.categoria,
        'cantidad': cantidad,
        'total': float(producto.precio) * cantidad
    }
    
    carrito = session.get('carrito', [])
    
    # Verificar si el producto ya está en el carrito
    for i, producto_en_carrito in enumerate(carrito):
        if producto_en_carrito['id'] == producto_id:
            # Actualizar cantidad y total
            carrito[i]['cantidad'] += cantidad
            carrito[i]['total'] = carrito[i]['precio'] * carrito[i]['cantidad']
            session['carrito'] = carrito
            return True, f'Se agregaron {cantidad} unidades más de "{producto.nombre}" al carrito.'
    
    # Si el producto no está en el carrito, agregarlo
    carrito.append(item)
    session['carrito'] = carrito
    return True, f'Se agregaron {cantidad} unidades de "{producto.nombre}" al carrito.'

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
    total = sum(float(p.get('total', p['precio'])) for p in carrito)
    return carrito, total

def limpiar_carrito():
    session['carrito'] = []