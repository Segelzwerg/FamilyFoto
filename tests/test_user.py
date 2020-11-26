from family_foto import add_user, Role
from family_foto.models.auth_token import AuthToken
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class UserTestCases(BaseTestCase):
    """
    Test the behaviour of the User Entity.
    """

    def test_all_user_asc(self):
        """
        Tests all users are returned in ascending order.
        """
        user_role = Role.query.filter_by(name='user').first()

        add_user('super_user', 'a', [user_role])
        add_user('another_user', 'a', [user_role])

        all_users = User.query.order_by(User.username.asc()).all()
        users = [[user.id, user.username] for user in all_users]
        self.assertListEqual(users, User.all_user_asc())

    def test_share_all_permission(self):
        """
        Tests the getter of all sharing permission.
        """
        user_role = Role.query.filter_by(name='user').first()

        user = add_user('user', '123', [user_role])
        other_user = add_user('other', '123', [user_role])
        user.share_all_with(other_user)
        self.assertTrue(user.has_general_read_permission(other_user),
                        msg=f'{other_user} has no permission to view photos of {user}')

    def test_create_auth_token(self):
        """
        Checks if an AuthToken is returned.
        """
        user_role = Role.query.filter_by(name='user').first()

        user = add_user('authy', 'geheim', [user_role])
        token = user.get_token()
        self.assertIsInstance(token, AuthToken)

    def test_get_auth_token(self):
        """
        Test getting an already existing token.
        """
        user_role = Role.query.filter_by(name='user').first()

        user = add_user('authy', 'geheim', [user_role])
        first_token = user.get_token()
        second_token = user.get_token()
        self.assertIsInstance(first_token, AuthToken)
        self.assertIsInstance(second_token, AuthToken)
        self.assertEqual(first_token, second_token)
