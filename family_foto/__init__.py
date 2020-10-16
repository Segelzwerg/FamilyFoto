import os
from typing import Any, Mapping

import flask_uploads
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

login_manager = LoginManager()


def create_app(test_config: (None, Mapping[str, Any]) = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'very-secret-key',
        DATABASE_URL_TEMPLATE='sqlite:///{instance_path}/app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOADED_PHOTOS_DEST_TEMPLATE='{instance_path}/photos',
        UPLOADED_VIDEOS_DEST_TEMPLATE='{instance_path}/videos',
        RESIZED_DEST_TEMPLATE='{instance_path}/resized-images'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or app.config[
        'DATABASE_URL_TEMPLATE'].format(instance_path=app.instance_path)
    app.config['UPLOADED_PHOTOS_DEST'] = app.config['UPLOADED_PHOTOS_DEST_TEMPLATE'].format(
        instance_path=app.instance_path)
    app.config['UPLOADED_VIDEOS_DEST'] = app.config['UPLOADED_VIDEOS_DEST_TEMPLATE'].format(
        instance_path=app.instance_path)
    app.config['RESIZED_DEST'] = app.config['RESIZED_DEST_TEMPLATE'].format(instance_path=app.instance_path)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    toolbar = DebugToolbarExtension(app)

    from family_foto.api import api
    app.register_blueprint(api)

    from family_foto.main import main
    app.register_blueprint(main)

    from family_foto.models import db
    db.init_app(app)
    db.app = app
    db.create_all()

    login_manager.init_app(app)

    from family_foto.main import photos, videos
    flask_uploads.configure_uploads(app, (photos, videos))

    from family_foto.main import add_user
    add_user('admin', 'admin')

    return app
