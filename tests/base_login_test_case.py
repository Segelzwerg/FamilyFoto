from flask_login import current_user

from tests.base_test_case import BaseTestCase
from tests.test_utils.mocking import mock_user


class BaseLoginTestCase(BaseTestCase):
    """
    Test Case that provides a logged in user mock.
    """

    def setUp(self):
        super().setUp()
        mock_user(self, 'marcel', 'user')
        current_user.active = True

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()
