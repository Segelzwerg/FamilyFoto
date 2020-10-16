from unittest.mock import patch

from family_foto.web import add_user
from tests.base_test_case import BaseTestCase


class BaseLoginTestCase(BaseTestCase):
    """
    Test Case that provides a logged in user mock.
    """

    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        user = add_user('marcel', '1234')
        self.mock_current_user.return_value = user
        self.mock_current_user.id = user.id

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()
