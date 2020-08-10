from family_foto.app import add_user
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
            self.assertNotIn('lea', [user.username for user in User.query.all()])

            add_user('lea', '12345')
            self.assertIn('lea', [user.username for user in User.query.all()])

    def test_duplicate_user(self):
        """
        Tests that a user can be added only once.
        """
        with self.client:
            self.assertNotIn('lea', [user.username for user in User.query.all()])

            add_user('lea', '12345')
            add_user('lea', '12345')
            self.assertEqual(1, [user.username for user in User.query.all()].count('lea'))
