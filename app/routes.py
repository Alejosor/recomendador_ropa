from flask import Blueprint, render_template
from popularidad import obtener_top_productos

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = obtener_top_productos()
    return render_template('index.html', productos=productos)
