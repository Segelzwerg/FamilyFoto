from werkzeug.http import HTTP_STATUS_CODES

from family_foto.api import success_response
from family_foto.errors import UploadError
from tests.base_test_case import BaseTestCase


class SuccessTestCase(BaseTestCase):
    """
    Tests the creation of API success response.
    """

    def test_success_response(self):
        """
        Tests creation without partial error.
        """
        expected_response = {'success': HTTP_STATUS_CODES.get(200)}
        self.assertDictEqual(expected_response, success_response([]).json)

    def test_success_response_with_partial_error(self):
        """
        Tests creation with partial error.
        """
        error = UploadError('test.file', 'Invalid')
        expected_response = {'success': HTTP_STATUS_CODES.get(200), 'error': ['Invalid']}
        self.assertDictEqual(expected_response, success_response([error]).json)
