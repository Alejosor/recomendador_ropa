from app import db
from app.models.product import Product
from app.models.venta import Venta
from app.models.venta_detail import VentaDetail
from app.models.user import User
import pandas as pd
import numpy as np

def get_products_data():
    products = Product.query.all()
    products_data = []

    for product in products:
        products_data.append({
            "id": product.id,
            "nombre": product.nombre,
            "categoria": product.categoria,
            "precio": float(product.precio),
            "cant_ventas": product.cant_ventas,
        })
    return pd.DataFrame(products_data)
def get_sales_data():
    sales = Venta.query.all()
    sales_data = []
    for sale in sales: 
        sales_data.append({
            "id": sale.id,
            "id_user": sale.id_user,
            "fecha": sale.fecha,
            "total": float(sale.total),
        })
    return pd.DataFrame(sales_data)
def get_sales_details_data():
    details = VentaDetail.query.all()
    details_data = []
    for detail in details:
        details_data.append({
            "id": detail.id,
            "id_venta": detail.id_venta,
            "id_product": detail.id_product,
            "cant": detail.cant,
            "unit_price": float(detail.unit_price),
        })
    return pd.DataFrame(details_data)
def get_user_purchase_history(user_id):
    user_sales = Venta.query.filter_by(id_user=user_id).all()
    sale_ids = [sale.id for sale in user_sales]
    if not sale_ids:
        return pd.DataFrame()
    purchase_history = VentaDetail.query.filter(VentaDetail.id_venta.in_(sale_ids)).all()
    history_data = []
    for purchase in purchase_history:
        history_data.append({
            "id_venta": purchase.id_venta,
            "id_product": purchase.id_product,
            "cant": purchase.cant,
        })
    return pd.DataFrame(history_data)
def get_product_categories():
    products = Product.query.all()
    categories = {}
    for product in products:
        categories[product.id] = product.categoria 
    return categories