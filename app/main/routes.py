from flask import render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from flask import redirect, url_for, session
from app.main import bp
from app.models.user import User
from app.models.game import Game
from app import db
from app import socketio

class PlayerForm(FlaskForm):
    game = IntegerField('Enter Game Code', validators=[DataRequired()])
    name = StringField('Enter Name', validators=[DataRequired(), Length(1, 20)])
    passcode = PasswordField('Enter Password',  validators=[DataRequired()])
    submit = SubmitField('Submit')

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = PlayerForm()
    if request.method =="POST" and form.validate():
        name = form.name.data
        passcode = form.passcode.data
        game = form.game.data
        record = User.query.get(name)
        if record != None:
            if record.password ==passcode:
                if not record.admit:
                    return(redirect(url_for('main.game', user = name)))
                else: 
                    return (redirect(url_for('main.start', user = name)))
            else:
                return "User already exists...Incorrect password!"
        else:
            new = User(code=game, name = name, password=passcode)
            db.session.add(new)
            db.session.commit()
            return(redirect(url_for('main.game', user = name)))
    return render_template('index.html', form = form)

@bp.route('/game/<user>', methods=['GET', 'POST'])
def game(user):
    if request.method =="POST":
        return(redirect(url_for('main.start', user = user)))
    if User.query.get(user).admit:
        return(redirect(url_for('main.start', user = user)))
    return render_template('lobby.html', user = user)

@bp.route('/clue/<user>', methods = ['GET', 'POST'])
def clue(user):
    hint = "Hi "+user 
    return jsonify(hint = hint, 
                   image ="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII")

@bp.route('/clue/play/<user>', methods=['GET', 'POST'])
def play(user):
    return render_template('game.html', user=user)

@bp.route('/start/play/<user>', methods=['GET', 'POST'])
def start(user):
    user_data = User.query.get(user)
    game_data = Game.query.get(user_data.code)
    if game_data.started:
        return(redirect(url_for('main.play', user = user)))
    rules=""
    return render_template('start.html', user=user, rules=rules)
    

