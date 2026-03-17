import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Bitte melden Sie sich an, um auf diese Seite zuzugreifen.'


def create_app(config_class=Config):
    app = Flask(__name__)
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance'), exist_ok=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main, auth, leg, members
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(leg.bp)
    app.register_blueprint(members.bp)

    with app.app_context():
        db.create_all()

    return app
