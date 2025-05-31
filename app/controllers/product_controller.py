from app.models.product import Product
from app import db
def obtener_top_productos(limit=10):
    return Product.query.order_by(Product.cant_ventas.desc()).limit(limit).all()

def obtener_producto_por_id(producto_id):
    return Product.query.get(producto_id)

def crear_producto(nombre, precio, categoria):
    producto = Product(nombre=nombre, precio=precio, categoria=categoria)
    db.session.add(producto)
    db.session.commit()
    return producto