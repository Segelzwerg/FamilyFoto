from family_foto.errors import RegistrationWarning
from tests.base_test_case import BaseTestCase


class ErrorTestCase(BaseTestCase):
    """
    Test the behaviour of the app's errors.
    """

    def test_registration_error(self):
        """
        Tests error during registration process.
        """
        field = 'password'
        reg_err = RegistrationWarning(field, ['This field is required.'])
        self.assertEqual(reg_err.message, f'This field is required: {field}')
