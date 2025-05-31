from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.controllers.product_controller import crear_producto
from app.models.admin import Admin
from functools import wraps

admin_bp = Blueprint('admin', __name__)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if session.get('rol') != 'admin':
            flash('Acceso denegado.')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/productos')
def lista_productos():
    from app.models.product import Product
    productos = Product.query.all()
    return render_template('admin/lista_productos.html', productos=productos)

@admin_bp.route('/admin/usuarios')
def lista_usuarios():
    from app.models.user import User  
    usuarios = User.query.all()
    return render_template('admin/lista_usuarios.html', usuarios=usuarios)

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        admin = Admin.query.filter_by(correo=correo, password=password).first()
        if admin:
            session.clear()
            session['usuario'] = admin.nombre
            session['rol'] = 'admin'
            flash('Bienvenido, administrador.')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales incorrectas.')
    return render_template('admin/login.html')

@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/admin/subir-producto', methods=['GET', 'POST'])
@admin_required
def subir_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        crear_producto(nombre, precio, categoria)
        flash('Producto subido correctamente.')
        return redirect(url_for('admin.subir_producto'))
    return render_template('admin/subir_producto.html')

@admin_bp.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_usuario(id):
    from app.models.user import User
    usuario = User.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo']
        
        from app import db
        db.session.commit()
        flash('Usuario actualizado correctamente.')
        return redirect(url_for('admin.lista_usuarios'))

    return render_template('admin/editar_usuario.html', usuario=usuario)

@admin_bp.route('/admin/editar_producto/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_producto(id):
    from app.models.product import Product
    producto = Product.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.categoria = request.form['categoria']
    
        from app import db
        db.session.commit()
        flash('Producto actualizado correctamente.')
        return redirect(url_for('admin.lista_productos'))

    return render_template('admin/editar_producto.html', producto=producto)
