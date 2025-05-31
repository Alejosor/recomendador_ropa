from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import csv
import uuid

auth = Blueprint('auth', __name__)

def guardar_usuario(nombre, email, password):
    with open('usuarios.csv', 'a', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([str(uuid.uuid4()), nombre, email, password])

def verificar_usuario(email, password):
    with open('usuarios.csv', 'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['email'] == email and fila['password'] == password:
                return fila
    return None

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        guardar_usuario(nombre, email, password)
        flash('Registro exitoso. Inicia sesión.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = verificar_usuario(email, password)
        if usuario:
            session['usuario'] = usuario['nombre']
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('main.index'))
        else:
            flash('Correo o contraseña incorrectos.')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada.')
    return redirect(url_for('main.index'))
