from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.controllers.product_controller import obtener_top_productos, obtener_producto_por_id
from app.controllers.carrito_controller import agregar_a_carrito, quitar_de_carrito, obtener_carrito, limpiar_carrito
from app.controllers.compra_controller import procesar_compra, obtener_compras_usuario
from app.ml.recommendation import get_recommendations, get_personalized_recommendations

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('usuario'):
        productos = get_personalized_recommendations(session['usuario'])
    else:
        productos = get_recommendations()
    return render_template('index.html', productos=productos)

@main.route('/agregar-carrito/<int:producto_id>')
def agregar_carrito(producto_id):
    exito, mensaje = agregar_a_carrito(producto_id)
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('main.index'))

@main.route('/carrito')
def ver_carrito():
    carrito, total = obtener_carrito()
    return render_template('carrito.html', carrito=carrito, total=total)

@main.route('/quitar-carrito/<int:indice>')
def quitar_carrito(indice):
    exito, mensaje = quitar_de_carrito(indice)
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('main.ver_carrito'))

@main.route('/comprar')
def comprar():
    if not session.get('usuario'):
        flash('Debes iniciar sesión para realizar una compra.', 'error')
        return redirect(url_for('auth.login'))
    exito, mensaje = procesar_compra()
    if exito:
        limpiar_carrito()
        return redirect(url_for('main.compra_exitosa'))
    else:
        flash(mensaje, 'error')
        return redirect(url_for('main.ver_carrito'))

@main.route('/compra-exitosa')
def compra_exitosa():
    if not session.get('usuario'):
        return redirect(url_for('auth.login'))
    return render_template('compra_exitosa.html')

@main.route('/mis-compras')
def mis_compras():
    if not session.get('usuario'):
        flash('Debes iniciar sesión para ver tus compras.', 'error')
        return redirect(url_for('auth.login'))
    compras = obtener_compras_usuario(session['usuario'])
    return render_template('mis_compras.html', compras=compras)