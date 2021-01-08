from sqlite3 import OperationalError
from unittest.mock import patch, Mock

from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class AddUserTestCase(BaseTestCase):
    """
    Test case for adding users.
    """

    def test_add_user(self):
        """
        Tests if a new user can be added.
        """
        with self.client:
            if 'lea' in [user.username for user in User.query.all()]:
                lea = User.query.filter_by(username='lea').first()
                db.session.delete(lea)
                db.session.commit()
            self.assertNotIn('lea', [user.username for user in User.query.all()])
            user_role = Role.query.filter_by(name='user').first()

            add_user('lea', '12345', [user_role])
            self.assertIn('lea', [user.username for user in User.query.all()])

    def test_duplicate_user(self):
        """
        Tests that a user can be added only once.
        """
        with self.client:
            self.assertNotIn('lea', [user.username for user in User.query.all()])

            user_role = Role.query.filter_by(name='user').first()

            add_user('lea', '12345', [user_role])
            add_user('lea', '12345', [user_role])
            self.assertEqual(1, [user.username for user in User.query.all()].count('lea'))

    @patch('family_foto.models.db.session.commit',
           Mock(side_effect=OperationalError))
    def test_opertional_error(self):
        """
        Tests if an operational error is thrown.
        """
        user_role = Role.query.filter_by(name='user').first()
        user = add_user('test', 'test', [user_role])
        self.assertIsNone(user)
