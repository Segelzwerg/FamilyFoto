from flask_api import status
from flask_login import current_user

from family_foto.app import app
from tests.base_test_case import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_login_page_is_available(self):
        with app.test_client() as client:
            response = client.get('/login')
            self.assertTrue(status.is_success(response.status_code))

    def test_login(self):
        with self.client:
            response = self.client.post('/login',
                                        data={'username': 'marcel',
                                              'password': '1234'},
                                        follow_redirects=True)
            self.assertTrue(status.is_success(response.status_code))
            self.assertEqual(current_user.username, 'marcel')
            self.assertFalse(current_user.is_anonymous())
