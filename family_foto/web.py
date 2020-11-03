import flask_uploads
from flask import redirect, url_for, render_template, request, send_from_directory, abort, \
    current_app, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet
from werkzeug.datastructures import FileStorage

from family_foto import login_manager, RESIZED_DEST, UPLOADED_PHOTOS_DEST, UPLOADED_VIDEOS_DEST
from family_foto.forms.login_form import LoginForm
from family_foto.forms.photo_sharing_form import PhotoSharingForm
from family_foto.forms.upload_form import UploadForm
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings
from family_foto.models.video import Video

web_bp = Blueprint('web', __name__)

VIDEOS = ('mp4',)
photos = UploadSet('photos', flask_uploads.IMAGES)
videos = UploadSet('videos', VIDEOS)


def add_user(username: str, password: str) -> User:
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
        return exists

    user_settings = UserSettings(user_id=user.id)
    user.settings = user_settings

    db.session.add(user_settings)
    db.session.add(user)
    db.session.commit()
    log.info(f'{user.username} registered.')
    return user


@web_bp.route('/')
@web_bp.route('/index')
def index():
    """
    Launches the index page.
    """
    return render_template('index.html', user=current_user)


@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Launches the login page.
    It redirects to index if an user already logged in or invalid user credentials.
    Otherwise launches login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            log.warning(f'{form.username.data} failed to log in')
            return redirect(url_for('web.login'))
        login_user(user, remember=form.remember_me.data)
        log.info(f'{user.username} logged in successfully')
        return redirect(url_for('web.index'))
    return render_template('login.html', title='Sign In', form=form)


@web_bp.route('/logout', methods=['GET'])
def logout():
    """
    Logs the current user out and redirects to index.
    """
    username = current_user.username
    logout_user()
    log.info(f'{username} logged out.')
    return redirect(url_for('web.index'))


@web_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Uploads a photo or with no passed on renders uploads view.
    """
    if 'file' in request.files:
        file: FileStorage = request.files['file']
        if 'image' in file.content_type:
            filename = photos.save(file)
            photo = Photo(filename=filename, user=current_user.id,
                          url=photos.url(filename))
            db.session.add(photo)
        elif 'video' in file.content_type:
            filename = videos.save(file)
            video = Video(filename=filename, user=current_user.id,
                          url=videos.url(filename))
            db.session.add(video)
        else:
            abort(400, f'file type {file.content_type} not supported.')
        db.session.commit()
        log.info(f'{current_user.username} uploaded {filename}')
    form = UploadForm()
    return render_template('upload.html', form=form, user=current_user, title='Upload')


@web_bp.route('/image/<filename>', methods=['GET', 'POST'])
@login_required
def image_view(filename):
    """
    Displays an photo in the image viewer.
    """
    log.info(f'{current_user.username} requested image view of {filename}')
    form = PhotoSharingForm()
    file = File.query.filter_by(filename=filename).first()

    if request.form.get('share_with'):
        users_share_with = [User.query.get(int(user_id)) for user_id in request.form.getlist(
            'share_with')]
        log.info(f'{current_user} requests to share photos with {users_share_with}')
        file.share_with(users_share_with)
        db.session.commit()

    form.share_with.choices = User.all_user_asc()
    form.share_with.data = [str(other_user_id) for
                            other_user_id in [current_user.settings.share_all_id]]
    if not file.has_read_permission(current_user):
        abort(401)
    return render_template('image.html', user=current_user, photo=file, form=form)


@web_bp.route('/photo/<filename>')
@web_bp.route('/_uploads/photos/<filename>')
@login_required
def uploaded_file(filename):
    """
    Returns path of the original photo.
    :param filename: name of the file
    """
    log.info(f'{current_user.username} requested '
             f'{current_app.config[UPLOADED_PHOTOS_DEST]}/{filename}')
    return send_from_directory(current_app.config[UPLOADED_PHOTOS_DEST], filename)


@web_bp.route('/_uploads/videos/<filename>')
@web_bp.route('/videos/<filename>')
@login_required
def get_video(filename):
    """
    Returns path of the original video.
    :param filename: name of the file
    """
    log.info(f'{current_user.username} requested '
             f'{current_app.config[UPLOADED_VIDEOS_DEST]}/{filename}')
    return send_from_directory(current_app.config[UPLOADED_VIDEOS_DEST], filename)


@web_bp.route('/resized-images/<filename>')
@login_required
def resized_photo(filename):
    """
    Returns the path resized image.
    :param filename: name of the resized photo
    """
    log.info(f'{current_user.username} requested {current_app.config[RESIZED_DEST]}/{filename}')
    return send_from_directory(current_app.config[RESIZED_DEST], filename)


@web_bp.route('/gallery', methods=['GET'])
@login_required
def gallery():
    """
    Shows all pictures requested
    """
    user_media = current_user.get_media()
    return render_template('gallery.html', media=user_media)


@web_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    Handles all user settings requests.
    """
    form = PhotoSharingForm()
    if request.form.get('share_with'):
        users_share_with = [User.query.get(int(user_id)) for user_id in request.form.getlist(
            'share_with')]
        log.info(f'{current_user} requests to share photos with {users_share_with}')
        current_user.share_all_with(users_share_with)
        db.session.commit()
    form.share_with.choices = User.all_user_asc()
    form.share_with.data = [str(other_user_id) for
                            other_user_id in [current_user.settings.share_all_id]]
    return render_template('user-settings.html',
                           user=current_user,
                           form=form)


@login_manager.user_loader
def load_user(user_id: int):
    """
    Loads a user from the database.
    :param user_id:
    :return: An user if exists.
    """
    return User.query.get(int(user_id))
