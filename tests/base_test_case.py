from flask_testing import TestCase

from family_foto.app import app
from family_foto.models import db
from family_foto.models.user import User


# pylint: disable=invalid-name
class BaseTestCase(TestCase):
    """
    Basic Test Case that setups the flask app with a db.
    """

    def create_app(self):
        app.config.from_object('family_foto.config.TestConfiguration')

        return app

    def setUp(self):
        db.create_all()
        user = User(username='marcel')
        user.set_password('1234')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
