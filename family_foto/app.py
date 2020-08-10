from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.datastructures import FileStorage

from family_foto.config import Config
from family_foto.forms.login_form import LoginForm
from family_foto.forms.upload_form import UploadForm
from family_foto.models import db
from family_foto.models.photo import Photo
from family_foto.models.user import User

app = Flask(__name__, template_folder='../templates')
app.config.from_object('family_foto.config.Config')

db.init_app(app)
db.app = app
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/')
def index():
    """
    Launches the index page.
    """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Launches the login page.
    It redirects to index if an user already logged in or invalid user credentials.
    Otherwise launches login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    """
    Logs the current user out and redirects to index.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Uploads a photo or with no passed on renders uploads view.
    """
    if 'file' in request.files:
        file: FileStorage = request.files['file']
        if 'image' in file.content_type:
            filename = photos.save(file)
            photo = Photo(filename=filename, user=current_user.id)
            db.session.add(photo)
            db.session.commit()
            flash(f"{filename} saved.")
    form = UploadForm()
    return render_template('upload.html', form=form)


@login_manager.user_loader
def load_user(user_id: int):
    """
    Loads a user from the database.
    :param user_id:
    :return: An user if exists.
    """
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
