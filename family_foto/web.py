from flask import redirect, url_for, render_template, request, send_from_directory, abort, \
    current_app, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage

from family_foto.const import RESIZED_DEST, UPLOADED_PHOTOS_DEST, UPLOADED_VIDEOS_DEST
from family_foto.forms.login_form import LoginForm
from family_foto.forms.photo_sharing_form import PhotoSharingForm
from family_foto.forms.public_form import PublicForm
from family_foto.forms.register_form import RegisterForm
from family_foto.forms.upload_form import UploadForm
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.video import Video
from family_foto.utils.add_user import add_user
from family_foto.utils.protected import guest_user
from family_foto.utils.thumbnail_service import ThumbnailService

web_bp = Blueprint('web', __name__)

VIDEOS = ('mp4',)
photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos', VIDEOS)


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


@web_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a guest user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        guest_role = Role.query.filter_by(name='guest').first()
        user = add_user(username=form.username.data, password=form.password.data,
                        roles=[guest_role])
        log.info(f'{user.username} successfully registered with roles: {user.roles}')

    return render_template('register.html', title='Register', form=form)


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
    public_form = PublicForm(request.form)
    file = File.query.filter_by(filename=filename).first()

    if request.form.get('share_with'):
        users_share_with = [User.query.get(int(user_id)) for user_id in request.form.getlist(
            'share_with')]
        log.info(f'{current_user} requests to share photos with {users_share_with}')
        file.share_with(users_share_with)
        db.session.commit()

    if request.form.get('public'):
        file.protected = request.form.get('public') == 'y'
        db.session.commit()

    if public_form.public:
        file.protected = public_form.public.data
        db.session.commit()

    form.share_with.choices = User.all_user_asc()
    form.share_with.data = [str(other_user_id) for
                            other_user_id in [current_user.settings.share_all_id]]

    public_form.public.checked = file.protected
    public_form.public.render_kw = {'value': 'y' if file.protected else 'n'}
    if not file.has_read_permission(current_user):
        abort(401)
    thumbnail = ThumbnailService.generate(file, 400, 400)
    return render_template('image.html', user=current_user, photo=file,
                           thumbnail=thumbnail, form=form, public_form=public_form)


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
    thumbnails = [ThumbnailService.generate(file, 200, 200) for file in user_media]
    return render_template('gallery.html', media=zip(user_media, thumbnails), link_type='preview')


@web_bp.route('/public', methods=['GET'])
@guest_user
def protected_gallery():
    """
    Shows the protected gallery.
    """
    media = Photo.query.filter_by(protected=True)
    thumbnails = [ThumbnailService.generate(file, 200, 200) for file in media]
    return render_template('gallery.html', media=zip(media, thumbnails), link_type='direct')


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
