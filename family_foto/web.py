from typing import List

from flask import redirect, url_for, render_template, request, send_from_directory, abort, \
    Blueprint, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message

from family_foto.errors import PasswordError, RegistrationWarning
from family_foto.forms.ResetLinkForm import ResetLinkForm
from family_foto.forms.login_form import LoginForm
from family_foto.forms.photo_sharing_form import PhotoSharingForm
from family_foto.forms.public_form import PublicForm
from family_foto.forms.register_form import RegisterForm
from family_foto.forms.reset_pwd_form import ResetPasswordForm
from family_foto.forms.upload_form import UploadForm
from family_foto.front_end_wrapper.utils.splitter import Splitter
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.approval import Approval
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.reset_link import ResetLink
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.services.thumbnail_service import generate
from family_foto.services.upload_service import UploadService
from family_foto.utils.add_user import add_user
from family_foto.utils.protected import is_active, guest_user

web_bp = Blueprint('web', __name__)


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
    if form.submit.data and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            log.warning(f'{form.username.data} failed to log in')
            return redirect(url_for('web.login'))
        login_user(user, remember=form.remember_me.data)
        log.info(f'{user.username} logged in successfully')
        return redirect(url_for('web.index'))
    if form.reset.data:
        reset_form = ResetLinkForm()
        reset_form.username = form.username
        return redirect(url_for('web.request_reset_password'), code=307)
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

    # pylint: disable=no-member
    form_errors = [RegistrationWarning(field, msg) for field, msg in form.errors.items()]
    for err in form_errors:
        log.warning(err.message)
    return render_template('register.html', title='Register', form=form, e=form_errors)


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
    Uploads photo(s) or video(s) or with no passed on renders uploads view.
    """
    files = request.files.getlist('file')
    # pylint: disable=protected-access
    app = current_app._get_current_object()
    uploader = UploadService(files, current_user.id, app)
    upload_errors = uploader.upload()
    status_code = 200
    if len(upload_errors) == len(files):
        status_code = 400
    form = UploadForm()
    return render_template('upload.html', form=form, user=current_user, title='Upload',
                           e=upload_errors), status_code


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
    thumbnail = generate(file, 400, 400)
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
    user_media: List[File] = current_user.get_media()
    splitter = Splitter(user_media)
    years_sorted = splitter.sorted_years()
    return render_template('gallery.html', user=current_user, years=years_sorted,
                           link_type='preview')


@web_bp.route('/public', methods=['GET'])
@is_active
@guest_user
def protected_gallery():
    """
    Shows the protected gallery.
    """
    media = Photo.query.filter_by(protected=True)
    splitter = Splitter(media)
    years_sorted = splitter.sorted_years()
    return render_template('gallery.html', user=current_user, years=years_sorted,
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
                           e=[error] if error else [])


@web_bp.route('/reset-pwd', methods=['POST'])
def request_reset_password():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user.email is None:
            log.warning(f'{username} request new password, but did not provide any email.')
            return redirect(url_for('web.login'))
        link = ResetLink.generate_link(user)
        reset_url = url_for('web.reset_password', user_id=user.id, link_hash=link.link_hash)
        email = Message(subject='FamilyFoto password reset',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=[user.email],
                        body=reset_url)
        with current_app.mail.connect() as conn:
            log.info(f'Password reset link sent to {username}')
            conn.send(email)
        form = LoginForm()
        reset_form = ResetLinkForm()
        return render_template('login.html', title='Sign In', form=form, reset_form=reset_form)
    log.warning(f'User for username "{username}" could not be found.')
    return redirect(url_for('web.login'))


@web_bp.route('/reset-pwd/<user_id>/<link_hash>', methods=['GET', 'POST'])
def reset_password(user_id: int, link_hash: str):
    form = ResetPasswordForm()

    if link_hash is not None:
        link: ResetLink = ResetLink.query.filter_by(link_hash=link_hash).first()
        if int(user_id) != link.user_id:
            return redirect(url_for('web.index'))

        if form.validate_on_submit() and link.is_active():
            user = User.query.get(int(user_id))
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('web.login'))

        link.set_active()
        db.session.add(link)
        db.session.commit()
        return render_template('reset-pwd.html', user=current_user,
                               form=form)
