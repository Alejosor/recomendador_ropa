from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth_controller import crear_usuario, verificar_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['email']
        password = request.form['password']
        crear_usuario(nombre, correo, password)
        flash('Registro exitoso. Inicia sesión.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        password = request.form['password']
        usuario = verificar_usuario(correo, password)
        if usuario:
            session.clear()
            session['usuario'] = usuario.nombre
            session['rol'] = 'usuario'
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('main.index'))
        else:
            flash('Correo o contraseña incorrectos.')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada.')
    return redirect(url_for('main.index'))