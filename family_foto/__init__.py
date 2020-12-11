import os
from typing import Any

import flask_uploads
from flask import Flask
from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate

from family_foto.admin.admin_approval_view import AdminApprovalView
from family_foto.admin.admin_index_view import AdminHomeView
from family_foto.admin.admin_model_view import AdminModelView
from family_foto.const import UPLOADED_PHOTOS_DEST_RELATIVE, UPLOADED_VIDEOS_DEST_RELATIVE, \
    RESIZED_DEST_RELATIVE, RESIZED_DEST, ADMIN_LEVEL, USER_LEVEL, GUEST_LEVEL
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings
from family_foto.utils.add_user import add_user

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

    admin = Admin(app, name='FamilyFoto', template_mode='bootstrap4',
                  index_view=AdminHomeView(url='/admin'))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminModelView(User, db.session))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminModelView(File, db.session))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminModelView(Role, db.session))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminApprovalView(name='Approval',  # lgtm [py/call-to-non-callable]
                                     endpoint='approval'))  # lgtm [py/call-to-non-callable]

    _ = DebugToolbarExtension(app)

    from family_foto.api import api_bp
    app.register_blueprint(api_bp)

    from family_foto.web import web_bp
    app.register_blueprint(web_bp)

    if os.path.exists(app.instance_path + '/app.db'):
        Migrate(app, db)
    db.init_app(app)
    db.app = app
    db.create_all()

    login_manager.init_app(app)

    from family_foto.web import photos, videos
    flask_uploads.configure_uploads(app, (photos, videos))

    with app.app_context():
        add_roles()

    add_user('admin', 'admin', [Role.query.filter_by(name='admin').first()], active=True)

    return app


def add_roles() -> None:
    """
    Add the predefined roles.
    """
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin', level=ADMIN_LEVEL, description='Can basically do '
                                                                       'everything.')
        db.session.add(admin_role)
    if not Role.query.filter_by(name='user').first():
        user_role = Role(name='user', level=USER_LEVEL,
                         description='The default user case. Registration required.')
        db.session.add(user_role)
    if not Role.query.filter_by(name='guest').first():
        user_role = Role(name='guest', level=GUEST_LEVEL,
                         description='A user which only can view the protected gallery. '
                                     'Registration required.')
        db.session.add(user_role)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id: int):
    """
    Loads a user from the database.
    :param user_id:
    :return: An user if exists.
    """
    return User.query.get(int(user_id))
