from unittest.mock import patch

from family_foto.app import add_user
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class BaseLoginTestCase(BaseTestCase):
    """
    Test Case that provides a logged in user mock.
    """
    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        self.mock_current_user.return_value = add_user('marcel', '1234')

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()
