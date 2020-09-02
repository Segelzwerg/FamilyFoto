from family_foto.app import add_user
from family_foto.models import db
from family_foto.models.user_settings import UserSettings
from tests.base_test_case import BaseTestCase


class UserSettingsTestCase(BaseTestCase):
    """
    Tests the user settings behaviour.
    """

    def setUp(self):
        super().setUp()
        self.user = add_user('settings_user', 'settings')

    def test_relation(self):
        """
        Tests if the id are set correctly.
        """
        self.assertIsNotNone(self.user.settings)
        self.assertEqual(self.user.id, self.user.settings.user_id)

    def test_add_user_to_sharing(self):
        """
        Tests if the share with does work correctly.
        """
        other_user = add_user('lea', '1234')
        self.user.share_all_with(other_user)
        db.session.commit()
        settings = UserSettings.query.get(self.user.id)
        self.assertListEqual([other_user], settings.share_all)

    def test_add_multiple_users_to_sharing(self):
        """
        Tests sharing photos with multiple users.
        """
        first_user = add_user('first', '5678')
        second_user = add_user('second', '9876')
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
        other_user = add_user('other_user', '1234')
        self.user.share_all_with(other_user)
        self.user.share_all_with([])
        self.assertNotIn(other_user, self.user.settings.share_all)

    def test_raise_unshare(self):
        """
        Tests if error is raised if user is None.
        """
        with self.assertRaises(AttributeError):
            self.user.settings.revoke_sharing(None)
