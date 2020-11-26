import os
from typing import Any

import flask_uploads
from flask import Flask
from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

from family_foto.admin.AdminModelView import AdminModelView
from family_foto.const import UPLOADED_PHOTOS_DEST_RELATIVE, UPLOADED_VIDEOS_DEST_RELATIVE, \
    RESIZED_DEST_RELATIVE, RESIZED_DEST
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings

login_manager = LoginManager()


# pylint: disable=import-outside-toplevel
def create_app(test_config: dict[str, Any] = None, test_instance_path: str = None) -> Flask:
    """
    Create the Flask application.
    :param test_config: config override
    :param test_instance_path: instance path override
    :return: the configured app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, instance_path=test_instance_path)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'very-secret-key',
        DATABASE_URL_TEMPLATE='sqlite:///{instance_path}/app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOADED_PHOTOS_DEST_RELATIVE='photos',
        UPLOADED_VIDEOS_DEST_RELATIVE='videos',
        RESIZED_DEST_RELATIVE='resized-images'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or app.config[
        'DATABASE_URL_TEMPLATE'].format(instance_path=app.instance_path)
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.instance_path,
                                                      app.config[UPLOADED_PHOTOS_DEST_RELATIVE])
    app.config['UPLOADED_VIDEOS_DEST'] = os.path.join(app.instance_path,
                                                      app.config[UPLOADED_VIDEOS_DEST_RELATIVE])
    app.config[RESIZED_DEST] = os.path.join(app.instance_path,
                                            app.config[RESIZED_DEST_RELATIVE])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='FamilyFoto', template_mode='bootstrap4')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(File, db.session))
    admin.add_view(AdminModelView(Role, db.session))

    _ = DebugToolbarExtension(app)

    from family_foto.api import api_bp
    app.register_blueprint(api_bp)

    from family_foto.web import web_bp
    app.register_blueprint(web_bp)

    db.init_app(app)
    db.app = app
    db.create_all()

    login_manager.init_app(app)

    from family_foto.web import photos, videos
    flask_uploads.configure_uploads(app, (photos, videos))

    add_roles()

    add_user('admin', 'admin', [Role.query.filter_by(name='admin').first()])

    return app


def add_roles():
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin', description='Can basically do everything.')
        db.session.add(admin_role)
    if not Role.query.filter_by(name='user').first():
        user_role = Role(name='user', description='The default user case. Registration required.')
        db.session.add(user_role)
    db.session.commit()


def add_user(username: str, password: str, roles: [Role]) -> User:
    """
    This registers an user.
    :param username: name of the user
    :param password: plain text password
    :param roles: list of the roles the user has
    """
    user = User(username=username)
    user.set_password(password)
    exists = User.query.filter_by(username=username).first()
    if exists:
        log.warning(f'{user.username} already exists.')
        return exists

    user_settings = UserSettings(user_id=user.id)
    user.settings = user_settings
    user.roles = roles

    db.session.add(user_settings)
    db.session.add(user)
    db.session.commit()
    log.info(f'{user.username} registered.')
    return user


@login_manager.user_loader
def load_user(user_id: int):
    """
    Loads a user from the database.
    :param user_id:
    :return: An user if exists.
    """
    return User.query.get(int(user_id))
