from app import db

class VentaDetail(db.Model):
    __tablename__ = 'venta_detail'
    id = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    cant = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    venta = db.relationship('Venta', back_populates='detalles')
    producto = db.relationship('Product', back_populates='detalles')