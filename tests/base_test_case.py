import os

from flask_testing import TestCase

from family_foto import config
from family_foto.app import app, add_user
from family_foto.models import db


# pylint: disable=invalid-name
class BaseTestCase(TestCase):
    """
    Basic Test Case that setups the flask app with a db.
    """

    def create_app(self):
        app.config.from_object(config.TestConfiguration)
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        add_user('marcel', '1234')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if os.path.exists('../test.db'):
            os.remove('../test.db')
