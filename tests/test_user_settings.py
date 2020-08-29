from unittest.mock import patch

from flask_login import current_user

from family_foto.app import add_user
from family_foto.models import db
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings
from tests.base_test_case import BaseTestCase


class UserSettingsTestCase(BaseTestCase):
    """
    Tests the user settings behaviour.
    """

    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        self.mock_current_user.return_value = User(id=1,
                                                   username='marcel')

    def test_relation(self):
        user = add_user('new_user', '1234')
        self.assertIsNotNone(user.settings)
        self.assertEqual(user.id, user.settings.user_id)

    def test_add_user_to_sharing(self):
        other_user = User.query.filter_by(username='lea').first()
        if not other_user:
            other_user = add_user('lea', '1234')
        current_user.share_all_with(other_user)
        db.session.commit()
        shared_with = UserSettings.query.get(current_user.id)
        self.assertListEqual([other_user], shared_with.share_all)
