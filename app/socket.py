from flask_socketio import emit, SocketIO
from app import db
from app.models.user import User

socketio = SocketIO()

