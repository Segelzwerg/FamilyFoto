from flask_api import status

from tests.base_admin_test_case import BaseAdminTestCase


class PromoteTestCase(BaseAdminTestCase):
    """
    Test promotion of users.
    """

    def test_route(self):
        """
        Tests the route exists.
        """
        response = self.client.get('/admin/promote', follow_redirects=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
