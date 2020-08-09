from flask_api import status
from flask_login import current_user

from family_foto.app import app
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class LoginTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user = User(username='marcel')
        user.set_password('1234')
        self.db.session.add(user)
        self.db.session.commit()
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
            self.assertFalse(current_user.is_anonymous)

    def test_login_fails(self):
        with self.client:
            response = self.client.post('/login',
                                        data={'username': 'marcel',
                                              'password': '12345'},
                                        follow_redirects=True)
            self.assertTrue(status.is_success(response.status_code))
            self.assertTrue(current_user.is_anonymous)
