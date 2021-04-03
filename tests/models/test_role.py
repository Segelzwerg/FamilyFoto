from family_foto import Role
from tests.base_test_case import BaseTestCase


class TestRoleCase(BaseTestCase):
    """
    Tests the functionalities of a role.
    """

    def test_str(self):
        """
        Tests str method.
        """
        role = Role(name='admin')
        self.assertEqual(str(role), 'admin')
