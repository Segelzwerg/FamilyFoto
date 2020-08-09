from flask_testing import TestCase
from family_foto.app import app
from family_foto.models import db


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('family_foto.config.TestConfiguration')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
