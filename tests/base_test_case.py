import os

from flask_testing import TestCase

from family_foto import config
from family_foto.app import app, add_user, db
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings


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
        db.session.close()
        db.drop_all()
        db.create_all()

        User.query.delete()
        UserSettings.query.delete()

        add_user('marcel', '1234')

    def tearDown(self):
        db.session.close()
        db.drop_all()
        if os.path.exists('../test.db'):
            os.remove('../test.db')

    def test_setup(self):
        """
        Tests the test database is clean before each test.
        """
        user = User.query.filter_by(username='marcel').first()
        settings = UserSettings.query.filter_by(user_id=user.id).first()

        self.assertIsNotNone(user.settings)
        self.assertEqual(user, settings.user)
