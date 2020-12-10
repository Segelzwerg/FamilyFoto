from flask_api import status

from tests.base_admin_test_case import BaseAdminTestCase


class TestUserApproval(BaseAdminTestCase):
    """
    Tests the approval of the admin for new users.
    """

    def test_route(self):
        """
        Tests the route /admin/approval exists.
        """
        with self.client:
            response = self.client.get('/admin/approval')
            self.assertEqual(status.HTTP_200_OK, response.status_code)
