from unittest.mock import patch

from tests.base_test_case import BaseTestCase


class BaseLoginTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        self.mock_current_user.return_value = User(id=1,
                                                   username='marcel')

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()