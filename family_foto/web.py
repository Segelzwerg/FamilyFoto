import hashlib

from flask import redirect, url_for, render_template, request, send_from_directory, abort, \
    Blueprint, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES

from family_foto.errors import UploadError, PasswordError
from family_foto.forms.login_form import LoginForm
from family_foto.forms.photo_sharing_form import PhotoSharingForm
from family_foto.forms.public_form import PublicForm
from family_foto.forms.register_form import RegisterForm
from family_foto.forms.upload_form import UploadForm
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.approval import Approval
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.video import Video
from family_foto.utils.add_user import add_user
from family_foto.utils.protected import is_active, guest_user
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
        approval = Approval(user=user.id)
        db.session.add(approval)
        db.session.commit()
        log.info(f'{user.username} successfully registered with roles: {user.roles}')
        return redirect(url_for('web.login'))

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
@is_active
@login_required
def upload():
    """
    Uploads a photo or with no passed on renders uploads view.
    """
    if 'file' in request.files:
        for file in request.files.getlist('file'):
            exists: File = File.query.filter_by(filename=file.filename).first()
            file_content = file.stream.read()
            file_hash = hashlib.sha3_256(file_content).hexdigest()
            file.stream.seek(0)
            if exists and file_hash == exists.hash:
                raise UploadError(exists.filename, f'File already exists: {exists.filename}')
            sub_folder = f'{file_hash[:2]}/{file_hash}'

            if 'image' in file.content_type:
                filename = photos.save(file, folder=sub_folder).split('/')[-1]
                photo = Photo(filename=filename, user=current_user.id,
                              hash=file_hash)
                db.session.add(photo)
            elif 'video' in file.content_type:
                filename = videos.save(file, folder=sub_folder).split('/')[-1]
                video = Video(filename=filename, user=current_user.id,
                              hash=file_hash)
                db.session.add(video)
            else:
                abort(400, f'file type {file.content_type} not supported.')
            db.session.commit()
            log.info(f'{current_user.username} uploaded {filename}')

    form = UploadForm()
    return render_template('upload.html', form=form, user=current_user, title='Upload')


@web_bp.route('/image/<file_hash>', methods=['GET', 'POST'])
@is_active
@login_required
def image_view(file_hash):
    """
    Displays an photo in the image viewer.
    """
    log.info(f'{current_user.username} requested image view of file with hash {file_hash}')
    form = PhotoSharingForm()
    public_form = PublicForm(request.form)
    file = File.query.filter_by(hash=file_hash).first()

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


@web_bp.route('/photos/<hash_group>/<file_hash>/<filename>')
@is_active
@login_required
def get_photo(hash_group, file_hash, filename):
    """
    Returns path of saved photo or video thumbnail.
    :param hash_group: first two chars of hash
    :param file_hash: hash of the file
    :param filename: name of file
    """
    file: File = File.query.filter_by(hash=file_hash).first()
    if not file.has_read_permission(current_user):
        log.warning(F'{current_user.username} tried to access {file.filename} without permission.')
        abort(401)
    return send_from_directory(f'{current_app.instance_path}/photos/{hash_group}/{file_hash}',
                               filename)


@web_bp.route('/videos/<hash_group>/<file_hash>/<filename>')
@is_active
@login_required
def get_video(hash_group, file_hash, filename):
    """
    Returns path of saved video or video thumbnail.
    :param hash_group: first two chars of hash
    :param file_hash: hash of the file
    :param filename: name of file
    """
    file: File = File.query.filter_by(hash=file_hash).first()
    if not file.has_read_permission(current_user):
        log.warning(F'{current_user.username} tried to access {file.filename} without permission.')
        abort(401)
    directory = f'{current_app.instance_path}/videos/{hash_group}/{file_hash}'
    return send_from_directory(directory, filename)


@web_bp.route('/gallery', methods=['GET'])
@is_active
@login_required
def gallery():
    """
    Shows all pictures requested
    """
    user_media = current_user.get_media()
    thumbnails = [ThumbnailService.generate(file, 200, 200) for file in user_media]
    return render_template('gallery.html', user=current_user, media=zip(user_media, thumbnails),
                           link_type='preview')


@web_bp.route('/public', methods=['GET'])
@is_active
@guest_user
def protected_gallery():
    """
    Shows the protected gallery.
    """
    media = Photo.query.filter_by(protected=True)
    thumbnails = [ThumbnailService.generate(file, 200, 200) for file in media]
    return render_template('gallery.html', user=current_user, media=zip(media, thumbnails),
                           link_type='direct')


@web_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    Handles all user settings requests.
    """
    form = PhotoSharingForm()
    error = None
    if request.form.get('share_with'):
        users_share_with = [User.query.get(int(user_id)) for user_id in request.form.getlist(
            'share_with')]
        log.info(f'{current_user} requests to share photos with {users_share_with}')
        current_user.share_all_with(users_share_with)
        db.session.commit()
    elif new_password := request.form.get('new_password'):
        old_password = request.form.get('old_password')
        repeat_new_password = request.form.get('new_password_repeat')
        if current_user.check_password(old_password):
            if new_password == repeat_new_password:
                current_user.set_password(new_password)
                db.session.add(current_user)
                db.session.commit()
            else:
                error = PasswordError('New passwords does not match.')
        else:
            error = PasswordError('Old password is wrong.')
            log.warning(f'{current_user} tried to change password, but the old one was wrong.')

    form.share_with.choices = User.all_user_asc()
    form.share_with.data = [str(other_user_id) for
                            other_user_id in [current_user.settings.share_all_id]]
    return render_template('user-settings.html',
                           user=current_user,
                           form=form,
                           e=error)


@web_bp.errorhandler(UploadError)
def handle_upload_errors(exception):
    """
    Catches error during uploading
    :param exception: of what happened
    """
    return render_template('upload.html', form=UploadForm(), e=exception)
