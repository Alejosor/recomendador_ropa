from app.models.user import User
from app import db

def crear_usuario(nombre, correo, password):
    user = User(nombre=nombre, correo=correo, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def verificar_usuario(correo, password):
    user = User.query.filter_by(correo=correo, password=password).first()
    return user