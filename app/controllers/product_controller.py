from app.models.product import Product

def obtener_top_productos(limit=10):
    return Product.query.order_by(Product.cant_ventas.desc()).limit(limit).all()

def obtener_producto_por_id(producto_id):
    return Product.query.get(producto_id)