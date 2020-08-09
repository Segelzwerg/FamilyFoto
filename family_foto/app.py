from flask import Flask, redirect, url_for, flash, render_template
from flask_login import LoginManager, current_user, login_user

from family_foto.config import Config
from family_foto.forms.login_form import LoginForm
from models import db
from models import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
db.app = app
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
