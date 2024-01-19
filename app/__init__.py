from flask import Flask
import json
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO, emit
from app.extensions import db
from app.socket import *
from app.models.game import Game
from app.models.user import User
from app.models.team import Team

def create_app():
    app = Flask(__name__)
    app.config.from_file("../config.json", load=json.load)
    app.jinja_env.auto_reload = True
    socketio.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Initialize Flask extensions here
    bootstrap = Bootstrap5(app)
    # Flask-WTF requires this line
    csrf = CSRFProtect(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix = "/admin")

    return app