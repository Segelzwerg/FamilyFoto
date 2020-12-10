from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings
from tests.base_test_case import BaseTestCase


class UserCommitTestCase(BaseTestCase):
    """
    Tests committing a user.
    """

    def test_setup(self):
        """
        Tests the test database is clean before each test.
        """
        user = User.query.filter_by(username='marcel').first()
        settings = UserSettings.query.filter_by(user_id=user.id).first()

        self.assertIsNotNone(user.settings)
        self.assertEqual(user, settings.user)
