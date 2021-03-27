from family_foto.errors import RegistrationError
from tests.base_test_case import BaseTestCase


class ErrorTestCase(BaseTestCase):
    def test_registration_error(self):
        field = 'password'
        reg_err = RegistrationError(field, ['This field is required.'])
        self.assertEqual(reg_err.message, f'This field is required: {field}')
