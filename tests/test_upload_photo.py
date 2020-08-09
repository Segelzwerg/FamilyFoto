from io import BytesIO
from unittest.mock import patch

from flask_api import status

from tests.base_test_case import BaseTestCase


class PhotoUploadTestCase(BaseTestCase):
    """
    Test case for uploading photos.
    """

    def setUp(self):
        pass
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()

    def tearDown(self):
        pass
        self.patcher.stop()

    def test_upload(self):
        """
        Tests if a jpg can be uploaded.
        """
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.jpg"),
        )
        response = self.client.post('/upload',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
