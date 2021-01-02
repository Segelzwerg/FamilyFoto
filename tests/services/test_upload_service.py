from flask import current_app

from family_foto.errors import UploadError
from family_foto.models.file import File
from family_foto.services.upload_service import UploadService
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_test_case import BaseTestCase


class UploadServiceTestCase(BaseTestCase):
    """
    Tests the behavior of the upload service.
    """

    def test_no_user_id(self):
        """
        Tests if the initializations fails with no user id.
        """
        with self.assertRaises(UploadError):
            file = File(filename='test')
            UploadService([file], None, current_app)

    def test_invalid_user_id(self):
        """
        Tests if the initializations fails with an invalid user id.
        """
        with self.assertRaises(UploadError):
            file = File(filename='test')
            UploadService([file], -2, current_app)


class UserUploadServiceTestCase(BaseLoginTestCase):
    """
    Test the upload service with an authenticated user.
    """

    def test_invalid_user_id(self):
        """
        Tests if the initializations fails with an invalid user id.
        """
        file = File(filename='test')
        self.assertIsNotNone(UploadService([file], None, current_app))
