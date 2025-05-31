from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql+psycopg2://futbolera_user:LVlPwRImzV7FrkrCWjOpjuhpGAInEBz4'
        '@dpg-d0t7je49c44c7396r900-a.oregon-postgres.render.com:5432/futbolera'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    from .routes.routes import main
    from .routes.auth_routes import auth_bp
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)

    return app