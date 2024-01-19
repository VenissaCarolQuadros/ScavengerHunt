from app.extensions import db

class Team(db.Model):
    team = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer) 
    clue = db.Column(db.Integer, default = 0) 

    def __repr__(self):
        return f'Team "{self.team}">'