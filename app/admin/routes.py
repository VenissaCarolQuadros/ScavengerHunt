from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, MultipleFileField
from wtforms.validators import DataRequired, Length
from flask import redirect, url_for, current_app as app
from app.admin import bp
from app.models.game import Game
from app.models.user import User
from app.models.team import Team
from app import db, socketio
from flask_socketio import emit
from werkzeug.utils import secure_filename


class GameForm(FlaskForm):
    game = IntegerField('Enter Game Code', validators=[DataRequired()])
    passcode = PasswordField('Enter Password',  validators=[DataRequired()])
    submit = SubmitField('Create New Game/ Continue Game')
class FileForm(FlaskForm):
    files = MultipleFileField("Upload all relevant files here")
    submit = SubmitField('Upload')

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = GameForm()
    
    if request.method =="POST" and form.validate():
        game = form.game.data
        passcode = form.passcode.data
        record = Game.query.get(game)
        if record != None:
            if record.password ==passcode:
                return(redirect(url_for('admin.manage', game = game)))
            else:
                return "Game already exists...Incorrect password!"
        else:
            new = Game(code=game, password=passcode)
            db.session.add(new)
            db.session.commit()
            return (redirect(url_for('admin.manage', game=game)))
    return render_template('admin/index.html', form = form)

@bp.route('/manage/<game>', methods=['GET', 'POST'])
def manage(game):
    pending = User.query.filter_by(code = game, admit = False)
    pending_req =[p.name for p in pending]
    file_form = FileForm()
    accepted = User.query.filter_by(code = game, admit = True)
    accepted_req =[a.name for a in accepted]
    if request.method=="POST":
        print()
        if "start_game" not in request.form and not file_form.files.data:
            for name in list(request.form.keys())[1:]:
                user = User.query.get(name)
                user.admit = True
                db.session.commit()
                pending_req.remove(name)
                accepted_req.append(name)
                socketio.emit('accepted', {'user': name})
                break
        
        if file_form.files.data:
            for f in file_form.files.data:
                name = secure_filename(f.filename)
                if allowed_file(name):
                    f.save(app.config['UPLOAD_FOLDER']+"/"+name)
        if "start_game" in request.form:
            for name in accepted_req:
                user = User.query.get(name)
                team = request.form[name]
                user.team = team
                team_data = Team.query.get(team)
                if team_data==None:
                    new = Team(code=user.code, team=team)
                    db.session.add(new)
            game_data = Game.query.get(user.code)
            game_data.started = True
            db.session.commit()
            return (redirect(url_for('admin.monitor', game=game)))
    return render_template('admin/manage.html', pending = pending_req, accepted = accepted_req,  file_form=file_form)

@bp.route('/monitor/<game>', methods=['GET', 'POST'])
def monitor(game):
    return "Monitoring page"

@bp.route('setup', methods=['GET', 'POST'])
def setup():
    return "Setup page"


@socketio.on('requesting')
def requesting(data):
     socketio.emit("requested", data)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']