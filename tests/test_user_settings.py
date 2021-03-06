from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.user_settings import UserSettings
from tests.base_test_case import BaseTestCase


class UserSettingsTestCase(BaseTestCase):
    """
    Tests the user settings behaviour.
    """

    def setUp(self):
        super().setUp()
        self.user_role = Role.query.filter_by(name='user').first()

        self.user = add_user('settings_user', 'settings', [self.user_role])

    def test_repr(self):
        """
        Tests representation of user.
        """
        self.assertEqual('<UserSettings of <User settings_user>>', str(self.user.settings))

    def test_relation(self):
        """
        Tests if the id are set correctly.
        """
        self.assertIsNotNone(self.user.settings)
        self.assertEqual(self.user.id, self.user.settings.user_id)

    def test_user_is_allowed_to_view_sharing(self):
        """
        Tests if getter of permissions works correctly.
        """
        other_user = add_user('test', '123', [self.user_role])
        lea = add_user('lea', '1234', [self.user_role])

        self.user.share_all_with([other_user, lea])
        settings = UserSettings.query.filter_by(user_id=self.user.id).first()
        self.assertTrue(settings.has_all_sharing(other_user), msg=f'{other_user} is not in '
                                                                  f'{settings.share_all}')

    def test_add_user_to_sharing(self):
        """
        Tests if the share with does work correctly.
        """
        other_user = add_user('lea', '1234', [self.user_role])
        self.user.share_all_with(other_user)
        db.session.commit()
        settings = UserSettings.query.get(self.user.id)
        self.assertListEqual([other_user], settings.share_all)

    def test_add_multiple_users_to_sharing(self):
        """
        Tests sharing photos with multiple users.
        """
        first_user = add_user('first', '5678', [self.user_role])
        second_user = add_user('second', '9876', [self.user_role])
        user_list = [first_user, second_user]

        self.user.share_all_with(user_list)
        settings = UserSettings.query.get(self.user.id)

        self.assertListEqual(user_list, settings.share_all)

    def test_none_share(self):
        """
        This tests that an error is raised with sharing a none user.
        """
        with self.assertRaises(AttributeError):
            self.user.share_all_with(None)

    def test_unshare(self):
        """
        Tests if user can revoke sharing.
        """
        other_user = add_user('other_user', '1234', [self.user_role])
        self.user.share_all_with(other_user)
        self.user.share_all_with([])
        self.assertNotIn(other_user, self.user.settings.share_all)

    def test_raise_unshare(self):
        """
        Tests if error is raised if user is None.
        """
        with self.assertRaises(AttributeError):
            self.user.settings.revoke_sharing(None)
