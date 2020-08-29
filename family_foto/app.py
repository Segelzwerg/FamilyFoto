from logging.config import dictConfig
from typing import Optional

import flask_resize
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from flask.logging import create_logger
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.datastructures import FileStorage

from family_foto.forms.login_form import LoginForm
from family_foto.forms.upload_form import UploadForm
from family_foto.models import *
from family_foto.models.photo import Photo
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__, template_folder='../templates')
app.config.from_object('family_foto.config.Config')

db.init_app(app)
db.app = app
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

resize = flask_resize.Resize(app)

log = create_logger(app)


def add_user(username: str, password: str) -> Optional[User]:
    """
    This registers an user.
    :param username: name of the user
    :param password: plain text password
    """
    user = User(username=username)
    user.set_password(password)
    exists = User.query.filter_by(username=username).first()
    if exists:
        log.warning(f'{user.username} already exists.')
        return None

    settings = UserSettings(user_id=user.id)
    user.settings = settings

    db.session.add(settings)
    db.session.add(user)
    db.session.commit()
    log.info(f'{user.username} registered.')
    return user


add_user('admin', 'admin')


@app.route('/')
@app.route('/index')
def index():
    """
    Launches the index page.
    """
    return render_template('index.html', user=current_user)


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
            log.warning(f'{form.username.data} failed to log in')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        log.info(f'{user.username} logged in successfully')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    """
    Logs the current user out and redirects to index.
    """
    username = current_user.username
    logout_user()
    log.info(f'{username} logged out.')
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
            photo = Photo(filename=filename, user=current_user.id, url=photos.url(filename))
            db.session.add(photo)
            db.session.commit()
            log.info(f'{current_user.username} uploaded {filename}')
    form = UploadForm()
    return render_template('upload.html', form=form, user=current_user, title='Upload')


@app.route('/photo/<filename>')
@app.route('/_uploads/photos/<filename>')
@login_required
def uploaded_file(filename):
    """
    Returns path of the original photo.
    :param filename: name of the file
    """
    log.info(f'{current_user.username} requested {app.config["UPLOADED_PHOTOS_DEST"]}/{filename}')
    return send_from_directory(f'../{app.config["UPLOADED_PHOTOS_DEST"]}', filename)


@app.route('/resized-images/<filename>')
@login_required
def resized_photo(filename):
    """
    Returns the path resized image.
    :param filename: name of the resized photo
    """
    log.info(f'{current_user.username} requested /resized-images/{filename}')
    return send_from_directory('../resized-images',
                               filename)


@app.route('/gallery', methods=['GET'])
@login_required
def gallery():
    """
    Shows all pictures requested
    """
    user_photos = current_user.get_photos()
    return render_template('gallery.html', photos=user_photos)


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
