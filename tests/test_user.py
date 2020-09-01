from family_foto.app import add_user
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class UserTestCases(BaseTestCase):
    def test_all_user_asc(self):
        """
        Tests all users are returned in ascending order.
        """
        add_user('super_user', 'a')
        add_user('another_user', 'a')

        all_users = User.query.order_by(User.username.asc()).all()
        users = [[user.id, user.username] for user in all_users]
        self.assertListEqual(users, User.all_user_asc())
