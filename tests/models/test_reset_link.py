from family_foto import add_user, Role
from family_foto.models.reset_link import ResetLink

from tests.base_test_case import BaseTestCase


class ResetLinkTestCase(BaseTestCase):
    """
    Test case for the reset link model.
    """

    def setUp(self):
        super().setUp()
        self.user_role = Role.query.filter_by(name='user').first()
        self.user = add_user('forgetty', 'none', [self.user_role])

    def test_generation(self):
        """
        Tests if a reset link is created correctly.
        """
        link = ResetLink.generate_link(user=self.user)
        self.assertIsNotNone(link)
        self.assertIsNotNone(ResetLink.query.all()[0])
