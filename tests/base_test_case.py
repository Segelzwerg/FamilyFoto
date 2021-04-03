import os
from shutil import rmtree

import prometheus_client
from flask_testing import TestCase

import family_foto
from family_foto import add_user
from family_foto.models import db
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings


class BaseTestCase(TestCase):
    """
    Basic Test Case that setups the flask app with a db.
    """

    # a little hackery is neccessary for the tests to work, because prometheus does not clean
    # it self between tests.

    # pylint: disable=protected-access
    def create_app(self):
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')

        for collector, _ in tuple(prometheus_client.REGISTRY._collector_to_names.items()):
            prometheus_client.REGISTRY.unregister(collector)
        app = family_foto.create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_TRACK_MODIFICATIONS': True,
            # Since we want our unit tests to run quickly
            # we turn this down - the hashing is still done
            # but the time-consuming part is left out.
            'HASH_ROUNDS': 1,
            # Fake Mail Server.
            'MAIL_SERVER': 'localhost',
            'MAIL_PORT': 465,
            'MAIL_USERNAME': 'noreply@ff.de',
            'MAIL_PASSWORD': '1234',
            'MAIL_SUPPRESS_SEND': True,
            'ADMIN_MAIL': 'admin@family-foto.com'
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
        add_user('marcel', '1234', [user_role], email='marcel@family-foto.com')

    def tearDown(self):
        db.session.close()
        db.drop_all()
        rmtree(self.app.instance_path)
