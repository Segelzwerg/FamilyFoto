import os
from typing import Any

import flask_uploads
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

UPLOADED_PHOTOS_DEST = 'UPLOADED_PHOTOS_DEST'
UPLOADED_PHOTOS_DEST_RELATIVE = 'UPLOADED_PHOTOS_DEST_RELATIVE'

UPLOADED_VIDEOS_DEST = 'UPLOADED_VIDEOS_DEST'
UPLOADED_VIDEOS_DEST_RELATIVE = 'UPLOADED_VIDEOS_DEST_RELATIVE'

RESIZED_DEST = 'RESIZED_DEST'
RESIZED_DEST_RELATIVE = 'RESIZED_DEST_RELATIVE'

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

    _ = DebugToolbarExtension(app)

    from family_foto.api import api_bp
    app.register_blueprint(api_bp)

    from family_foto.web import web_bp
    app.register_blueprint(web_bp)

    from family_foto.models import db
    db.init_app(app)
    db.app = app
    db.create_all()

    login_manager.init_app(app)

    from family_foto.web import photos, videos
    flask_uploads.configure_uploads(app, (photos, videos))

    from family_foto.web import add_user
    add_user('admin', 'admin')

    return app
