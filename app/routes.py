from flask import Blueprint, render_template, session, redirect, url_for, flash
from popularidad import obtener_top_productos, obtener_producto_por_id
import csv
import uuid

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

@main.route('/comprar')
def comprar():
    if not session.get('usuario'):
        flash('Debes iniciar sesión para realizar una compra.', 'error')
        return redirect(url_for('auth.login'))

    carrito = session.get('carrito', [])
    if not carrito:
        flash('Tu carrito está vacío.', 'error')
        return redirect(url_for('main.ver_carrito'))

    id_orden = str(uuid.uuid4())
    nombre_usuario = session['usuario']

    with open('ordenes.csv', 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        for producto in carrito:
            writer.writerow([
                id_orden,
                nombre_usuario,
                producto['nombre'],
                producto['categoria'],
                producto['precio']
            ])

    session['carrito'] = []
    session['carrito'] = []
    return redirect(url_for('main.compra_exitosa'))

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

    usuario = session['usuario']
    compras = []

    try:
        with open('ordenes.csv', newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila['nombre_usuario'] == usuario:
                    compras.append(fila)
    except FileNotFoundError:
        compras = []

    return render_template('mis_compras.html', compras=compras)
