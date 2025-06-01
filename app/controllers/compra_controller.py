from flask import session
from app import db
from app.models.venta import Venta
from app.models.venta_detail import VentaDetail
from app.models.product import Product
from app.models.user import User

def procesar_compra():
    usuario_nombre = session.get('usuario')
    if not usuario_nombre:
        return False, "Usuario no autenticado."
    user = User.query.filter_by(nombre=usuario_nombre).first()
    if not user:
        return False, "Usuario no encontrado."
    carrito = session.get('carrito', [])
    if not carrito:
        return False, "El carrito está vacío."    
    # Calcular total usando el campo total de cada item
    total = sum(float(item['total']) for item in carrito)
    
    venta = Venta(id_user=user.id, total=total)
    db.session.add(venta)
    db.session.flush()  # Para obtener el id de la venta
    
    for item in carrito:
        cantidad = item.get('cantidad', 1)  # Usar la cantidad seleccionada
        detalle = VentaDetail(
            id_venta=venta.id,
            id_product=item['id'],
            cant=cantidad,  # Usar cantidad correcta
            unit_price=item['precio']
        )
        db.session.add(detalle)
        
        # Actualizar ventas del producto considerando la cantidad
        producto = Product.query.get(item['id'])
        if producto:
            producto.cant_ventas += cantidad  # Incrementar según cantidad
    
    db.session.commit()
    return True, "Compra realizada con éxito."

def obtener_compras_usuario(usuario_nombre):
    user = User.query.filter_by(nombre=usuario_nombre).first()
    if not user:
        return []
    compras = []
    for venta in user.ventas:
        for detalle in venta.detalles:
            compras.append({
                'id_venta': venta.id,
                'fecha': venta.fecha,
                'total': float(venta.total),
                'nombre_producto': detalle.producto.nombre,
                'categoria': detalle.producto.categoria,
                'cantidad': detalle.cant,
                'precio_unitario': float(detalle.unit_price)
            })
    return compras