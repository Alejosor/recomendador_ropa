from flask import Blueprint, render_template, session, redirect, url_for, flash
from popularidad import obtener_top_productos, obtener_producto_por_id

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = obtener_top_productos()
    return render_template('index.html', productos=productos)

@main.route('/agregar-carrito/<int:producto_id>')
def agregar_carrito(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        flash('Producto no encontrado.')
        return redirect(url_for('main.index'))

    if 'carrito' not in session:
        session['carrito'] = []

    carrito = session['carrito']
    carrito.append(producto)
    session['carrito'] = carrito
    flash(f'Se agregó "{producto["nombre"]}" al carrito.', 'success')
    return redirect(url_for('main.index'))

@main.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = sum(float(p['precio']) for p in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

@main.route('/quitar-carrito/<int:indice>')
def quitar_carrito(indice):
    carrito = session.get('carrito', [])
    if 0 <= indice < len(carrito):
        producto_quitado = carrito[indice]['nombre']
        carrito.pop(indice)
        session['carrito'] = carrito
        flash(f'Se eliminó "{producto_quitado}" del carrito.', 'error')
    else:
        flash('Índice inválido.', 'error')
    return redirect(url_for('main.ver_carrito'))