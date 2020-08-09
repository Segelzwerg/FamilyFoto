from flask_testing import TestCase

from family_foto.app import app
from family_foto.models import db


class BaseTestCase(TestCase):
    """
    Basic Test Case that setups the flask app with a db.
    """
    def create_app(self):
        app.config.from_object('family_foto.config.TestConfiguration')
        self.db = db
        return app

    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
