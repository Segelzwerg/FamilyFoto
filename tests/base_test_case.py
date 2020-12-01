import os
from shutil import rmtree

from flask_testing import TestCase

import family_foto
from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings


class BaseTestCase(TestCase):
    """
    Basic Test Case that setups the flask app with a db.
    """

    def create_app(self):
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        app = family_foto.create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_TRACK_MODIFICATIONS': True,
            # Since we want our unit tests to run quickly
            # we turn this down - the hashing is still done
            # but the time-consuming part is left out.
            'HASH_ROUNDS': 1
        }, instance_path)
        return app

    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

        User.query.delete()
        UserSettings.query.delete()

        family_foto.add_roles()
        user_role = Role.query.filter_by(name='user').first()
        add_user('marcel', '1234', [user_role])

    def tearDown(self):
        db.session.close()
        db.drop_all()
        rmtree(self.app.instance_path)

    def test_setup(self):
        """
        Tests the test database is clean before each test.
        """
        user = User.query.filter_by(username='marcel').first()
        settings = UserSettings.query.filter_by(user_id=user.id).first()

        self.assertIsNotNone(user.settings)
        self.assertEqual(user, settings.user)
