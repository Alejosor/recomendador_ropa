from app import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    cant_ventas = db.Column(db.Integer, default=0)

    detalles = db.relationship('VentaDetail', back_populates='producto')