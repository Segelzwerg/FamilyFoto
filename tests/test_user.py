from family_foto import add_user, Role
from family_foto.models.auth_token import AuthToken
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class UserTestCases(BaseTestCase):
    """
    Test the behaviour of the User Entity.
    """

    def setUp(self):
        self.admin_role: Role = Role.query.filter_by(name='admin').first()
        self.user_role: Role = Role.query.filter_by(name='user').first()
        self.user: User = add_user('user', '123', [self.user_role])

    def test_repr(self):
        """
        Tests representation of user.
        """
        self.assertEqual('<User user>', str(self.user))

    def test_all_user_asc(self):
        """
        Tests all users are returned in ascending order.
        """

        add_user('super_user', 'a', [self.user_role])
        add_user('another_user', 'a', [self.user_role])

        all_users = User.query.order_by(User.username.asc()).all()
        users = [[user.id, user.username] for user in all_users]
        self.assertListEqual(users, User.all_user_asc())

    def test_share_all_permission(self):
        """
        Tests the getter of all sharing permission.
        """

        other_user = add_user('other', '123', [self.user_role])
        self.user.share_all_with(other_user)
        self.assertTrue(self.user.has_general_read_permission(other_user),
                        msg=f'{other_user} has no permission to view photos of {self.user}')

    def test_create_auth_token(self):
        """
        Checks if an AuthToken is returned.
        """

        token = self.user.get_token()
        self.assertIsInstance(token, AuthToken)

    def test_get_auth_token(self):
        """
        Test getting an already existing token.
        """

        first_token = self.user.get_token()
        second_token = self.user.get_token()
        self.assertIsInstance(first_token, AuthToken)
        self.assertIsInstance(second_token, AuthToken)
        self.assertEqual(first_token, second_token)

    def test_user_has_role(self):
        """
        Tests if a user has role.
        """
        self.assertTrue(self.user.has_role('user'))

    def test_user_has_not_role(self):
        """
        Tests if a user has role.
        """
        self.assertFalse(self.user.has_role('admin'), f'{self.user.username} has role admin, '
                                                      f'but should only have '
                                                      f'{self.user_role.name}.')

    def test_user_has_at_least(self):
        """
        Tests if a user has at least user rights.
        """
        self.assertTrue(self.user.has_at_least_role(self.user_role.level))

    def test_admin_has_at_least_user(self):
        """
        Tests if a admin has at least user rights.
        """
        user = add_user('user', 'pass', [self.admin_role])
        self.assertTrue(user.has_at_least_role(self.user_role.level))

    def test_add_role(self):
        """
        Tests if adding a role works.
        """
        self.user.add_role(self.admin_role)
        self.assertTrue(self.user.has_at_least_role(self.admin_role.level))
