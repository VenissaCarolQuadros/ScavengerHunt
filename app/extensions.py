from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.game import Game
from app.models.user import User
