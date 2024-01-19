from app.extensions import db

class User(db.Model):
    code = db.Column(db.Integer)  
    name =db.Column(db.String(20), unique=True, primary_key=True)
    admit = db.Column(db.Boolean, default = False)
    team =db.Column(db.Integer, default=0)
    password =db.Column(db.String(20))

    def __repr__(self):
        return f'<User "{self.name}">'
    