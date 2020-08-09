import unittest

from flask_api import status

from family_foto.app import app


class LoginTestCase(unittest.TestCase):
    def test_login_page_is_available(self):
        with app.test_client() as client:
            response = client.get('/login')
            self.assertTrue(status.is_success(response.status_code))
