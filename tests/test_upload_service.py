from family_foto.errors import UploadError
from family_foto.models.file import File
from family_foto.services.upload_service import upload_file
from tests.base_test_case import BaseTestCase


class UploadServiceTestCase(BaseTestCase):
    """
    Tests the upload service.
    """

    def test_user_id_required(self):
        """
        Tests if an error is raised when no user id is given.
        """
        with self.assertRaises(UploadError):
            file = File(filename='test.jpg')
            upload_file(file)
