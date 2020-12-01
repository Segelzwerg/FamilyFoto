from tests.base_test_case import BaseTestCase
from tests.test_utils.mocking import mock_user


class BaseAdminTestCase(BaseTestCase):
    """
    Test case for admin mocked on current_user
    """

    def setUp(self):
        super().setUp()
        mock_user(self, 'admin', 'admin')

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()
