import os

from flask_api import status
from flask_login import current_user

from tests.base_login_test_case import BaseLoginTestCase


class ApiUploadTestCase(BaseLoginTestCase):
    """
    Tests the upload via API.
    """

    def test_upload_photo(self):
        token = current_user.get_token()
        filename = 'example.jpg'

        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                            filename)
        file = open(path, 'rb')
        data = dict(files=[(file, filename)])
        response = self.client.post('/api/upload',
                                    headers={'Authorization': f'Bearer {token.token}'},
                                    content_type='multipart/form-data',
                                    data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
