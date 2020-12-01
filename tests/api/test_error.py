from family_foto.api.errors import error_response
from tests.base_test_case import BaseTestCase


class ApiErrorTestCase(BaseTestCase):
    """
    Tests the error handling for the API.
    """

    def test_unknown_error(self):
        """
        Tests the unknown error.
        """
        response = error_response(1)
        json = response.json

        expected_json = {'error': 'Unknown error'}
        self.assertDictEqual(expected_json, json)

    def test_404(self):
        """
        Tests not found error.
        """
        response = error_response(404)
        json = response.json

        expected_json = {'error': 'Not Found'}
        self.assertDictEqual(expected_json, json)

    def test_401_with_custom_msg(self):
        """
        Tests unauthorized with custom message.
        """
        message = 'You shall not pass!'
        response = error_response(401, message)
        json = response.json

        expected_json = {'error': 'Unauthorized', 'message': message}
        self.assertDictEqual(expected_json, json)
