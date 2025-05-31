from app import db, create_app
from app.models.product import Product


app = create_app()

#Aca va el array de productos
productos =[
    {"nombre": "Balón Adidas Finale", "precio": 310.00, "categoria": "Balones"},
]

#Aca se cargan los productos a la db waaaa
with app.app_context():
    for p in productos:
        nuevo_producto = Product(
            nombre=p["nombre"],
            precio=p["precio"],
            categoria=p["categoria"]
        )
        db.session.add(nuevo_producto)
    db.session.commit()
    print("Productos cargados con éxito")
