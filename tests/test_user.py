from family_foto.app import add_user
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
        add_user('super_user', 'a')
        add_user('another_user', 'a')

        all_users = User.query.order_by(User.username.asc()).all()
        users = [[user.id, user.username] for user in all_users]
        self.assertListEqual(users, User.all_user_asc())

    def test_share_all_permission(self):
        """
        Tests the getter of all sharing permission.
        """
        user = add_user('user', '123')
        other_user = add_user('other', '123')
        user.share_all_with(other_user)
        self.assertTrue(user.has_general_read_permission(other_user),
                        msg=f'{other_user} has no permission to view photos of {user}')
