from app.extensions import db

class Game(db.Model):
    code = db.Column(db.Integer, primary_key=True, unique= True)
    started =db.Column(db.Boolean, default=False) 
    password =db.Column(db.String(20))

    def __repr__(self):
        return f'<Game "{self.code}">'
